# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

import requests

from payu_sdk.dto.auth import Auth
from payu_sdk.dto.order import Order
from payu_sdk.validators.response import (
    validate_payu_auth_success,
    validate_payu_create_order_success,
    validate_payu_get_payment,
    validate_payu_response,
)

API_URL = "https://secure.payu.com"
SANDBOX_AP_URL = "https://secure.snd.payu.com"


class PayU:
    sandbox: bool
    client_id: str
    client_secret: str
    pos_id: str
    email: str | None
    ext_customer_id: str | None
    authorized: Auth | None

    def __init__(self, client_id: str, client_secret: str, pos_id: str, email: str = None, ext_customer_id: str = None):
        self.sandbox = False
        self.authorized = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.email = email
        self.ext_customer_id = ext_customer_id
        self.pos_id = pos_id

    def use_sandbox(self, flag: bool = True) -> None:
        self.sandbox = flag

    def is_sandbox(self) -> bool:
        return self.sandbox

    def get_api_url(self) -> str:
        if not self.sandbox:
            return API_URL
        else:
            return SANDBOX_AP_URL

    def _build_url(self, endpoint: str) -> str:
        return self.get_api_url() + endpoint

    def is_authorized(self) -> bool:
        if isinstance(self.authorized, Auth) and not self.authorized.is_expired():
            return True
        return False

    def authorize(self) -> "PayU":
        if self.is_authorized():
            return self

        endpoint = "/pl/standard/user/oauth/authorize"
        # https://developers.payu.com/europe/docs/payment-flows/auth-and-order/#authorization-request
        if self.email and self.ext_customer_id:
            parameters = {
                "grant_type": "trusted_merchant",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "email": self.email,
                "ext_customer_id": self.ext_customer_id,
            }

        else:
            parameters = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        url = self._build_url(endpoint)

        response = requests.request("GET", url, params=parameters)
        response_body = json.loads(response.text)
        if not validate_payu_auth_success(response_body):
            raise ConnectionError("PayU Connection error")

        self.authorized = Auth(
            access_token=response_body["access_token"],
            token_type=response_body["token_type"],
            expires_in=int(response_body["expires_in"]),
            grant_type=response_body["grant_type"],
        )

        return self

    def create_order(self, order: Order) -> (str, str):
        """
        Creates order in PayU. If Succes you will recive PayU internal order ID and redirect URI to complete transaction.
        """
        if not self.is_authorized():
            raise ConnectionError("PayU Connection not authorized")
        endpoint = "/api/v2_1/orders"
        url = self._build_url(endpoint)

        headers = {
            "Authorization": "Bearer " + self.authorized.access_token,
            "Content-Type": "application/json",
        }
        order_dict = order.asdict()
        if order.cardOnFile is None:
            order_dict.pop("cardOnFile")

        payload = json.dumps(order_dict)
        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        validation, response_body = validate_payu_response(response)
        if validation:
            success, order_id, redirection_uri = validate_payu_create_order_success(response_body)
            if success:
                return order_id, redirection_uri

        # If nothing happend
        raise SystemError("Unknown Error")

    def get_payment(self) -> (str, str):
        """
        Get payment methods from PayU.
        """
        if not self.is_authorized():
            raise ConnectionError("PayU Connection not authorized")
        endpoint = "/api/v2_1/paymethods"
        url = self._build_url(endpoint)

        headers = {
            "Authorization": "Bearer " + self.authorized.access_token,
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers)

        validation, response_body = validate_payu_response(response)
        if validation:
            success, available_payments = validate_payu_get_payment(response_body)
            if success:
                return available_payments
        # If nothing happend
        raise SystemError("Unknown Error")

    def delete_card(self, token) -> bool:
        """
        Delete card from PayU for trusted merchant.
        """
        if not self.is_authorized():
            raise ConnectionError("PayU Connection not authorized")
        endpoint = f"/api/v2_1/tokens/{token}"
        url = self._build_url(endpoint)

        headers = {
            "Authorization": "Bearer " + self.authorized.access_token,
            "Content-Type": "application/json",
        }

        response = requests.request("DELETE", url, headers=headers)
        if response.status_code in [200, 201, 202, 203, 204]:
            return True
        return False

    def add_card(self, token, ip, first_transaction_id) -> bool:
        payload = json.dumps(
            {
                "customerIp": ip,
                "merchantPosId": self.pos_id,
                "description": "Saving card",
                "currencyCode": "PLN",
                "totalAmount": "0",
                "cardOnFile": "FIRST",
                "extOrderId": str(first_transaction_id),
                "buyer": {
                    "email": self.email,
                },
                "payMethods": {"payMethod": {"value": token, "type": "CARD_TOKEN"}},
            }
        )

        if not self.is_authorized():
            raise ConnectionError("PayU Connection not authorized")
        endpoint = "/api/v2_1/orders"
        url = self._build_url(endpoint)

        headers = {
            "Authorization": "Bearer " + self.authorized.access_token,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        validation, response_body = validate_payu_response(response)

        if validation:
            success, order_id, redirection_uri = validate_payu_create_order_success(response_body)
            if success:
                return success

        # If nothing happend
        raise SystemError("Unknown Error")

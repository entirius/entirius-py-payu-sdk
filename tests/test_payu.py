# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

import pytest

from payu_sdk import PayU
from payu_sdk.dto.auth import Auth
from payu_sdk.dto.buyer import Buyer
from payu_sdk.dto.order import Order
from payu_sdk.dto.pay_method import PayMethods
from payu_sdk.dto.product import Product

# Sandbox credentials come from the environment; the integration test skips without them.
# See https://developers.payu.com/en/overview.html#sandbox
SANDBOX_CLIENT_ID = os.environ.get("PAYU_SANDBOX_CLIENT_ID")
SANDBOX_CLIENT_SECRET = os.environ.get("PAYU_SANDBOX_CLIENT_SECRET")
SANDBOX_POS_ID = os.environ.get("PAYU_SANDBOX_POS_ID")
EMAIL = "test1222@testtest.pl"
FIRST_TRANSACTION_ID = "1010003123"
EXT_CUSTOMER_ID = "123cfa6d-8c3b-47a8-a697-6c13d0f5f55b"

USE_SANDBOX = True

pytestmark = pytest.mark.skipif(
    not (SANDBOX_CLIENT_ID and SANDBOX_CLIENT_SECRET and SANDBOX_POS_ID),
    reason="PayU sandbox credentials not set (PAYU_SANDBOX_* env vars)",
)


def test_authorize():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
    )
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()

    assert isinstance(payu.authorized, Auth)


def test_create_order_normal():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
    )
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()

    buyer = Buyer(
        email=EMAIL,
        phone="654111654",
        firstName="John",
        lastName="Doe",
        language="pl",
    )

    products = [
        Product(name="Wireless Mouse for Laptop", unitPrice="15000", quantity="1"),
        Product(name="HDMI cable", unitPrice="6000", quantity="1"),
    ]

    order = Order(
        notifyUrl="https://example.com/notify",
        continueUrl="https://example.com/admin",
        customerIp="127.0.0.1",
        merchantPosId=SANDBOX_POS_ID,
        description="RTV market",
        currencyCode="PLN",
        totalAmount="21000",
        buyer=buyer,
        products=products,
    )

    order_id, redirect_uri = payu.create_order(order)
    assert isinstance(order_id, str)
    assert isinstance(redirect_uri, str)


def test_create_order_card(payu):
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()

    buyer = Buyer(
        email=EMAIL,
        phone="654111654",
        firstName="John",
        lastName="Card",
        language="pl",
    )

    products = [
        Product(name="Wireless Mouse for Laptop", unitPrice="15000", quantity="1"),
        Product(name="HDMI cable", unitPrice="6000", quantity="1"),
    ]

    card_token = get_card_token()
    pay_methods = PayMethods.factory("CARD_TOKEN", card_token)
    order = Order(
        notifyUrl="https://example.com/notify",
        customerIp="127.0.0.1",
        merchantPosId=SANDBOX_POS_ID,
        description="RTV market",
        currencyCode="PLN",
        totalAmount="21000",
        buyer=buyer,
        cardOnFile="FIRST",
        products=products,
        payMethods=pay_methods,
    )
    order_id, redirect_uri = payu.create_order(order)
    assert isinstance(order_id, str)
    assert isinstance(redirect_uri, str)


def test_create_order_card_for_for_client_credentials():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
    )
    test_create_order_card(payu)


def test_create_order_card_for_trusted_merchant():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
        email=EMAIL,
        ext_customer_id=EXT_CUSTOMER_ID,
    )
    test_create_order_card(payu)
    test_get_payment(payu)


def test_get_payment(payu):
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()
    available_payments = payu.get_payment()
    assert isinstance(available_payments, dict)


def test_add_payment(payu):
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()
    token = "TOK_EXAMPLE"  # ephemeral sandbox card token; provide a fresh one when running locally
    payu.add_card(token)


def test_get_payment_for_client_credentials():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
    )
    test_get_payment(payu)


def test_get_payment_for_trusted_merchant():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
        email=EMAIL,
        ext_customer_id=EXT_CUSTOMER_ID,
    )
    test_get_payment(payu)


def test_add_payu_card_for_trusted_merchant():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
        email=EMAIL,
        ext_customer_id=EXT_CUSTOMER_ID,
    )
    test_add_payment(payu)


def test_delete_payu_card_for_trusted_merchant():
    payu = PayU(
        client_id=SANDBOX_CLIENT_ID,
        client_secret=SANDBOX_CLIENT_SECRET,
        pos_id=SANDBOX_POS_ID,
        email=EMAIL,
        ext_customer_id=EXT_CUSTOMER_ID,
    )
    payu.use_sandbox(USE_SANDBOX)
    payu.authorize()
    token = "TOKC_EXAMPLE"  # ephemeral sandbox card token; provide a fresh one when running locally
    payu.delete_card(token)


def get_card_token():
    # https://replit.com/@PayU/Secure-Form
    # U need new token every few minutes
    f = open("./card_token")
    return f.read()

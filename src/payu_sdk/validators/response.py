# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from requests import Response


def validate_payu_response(response: Response) -> (bool, dict):
    response_body = json.loads(response.text)
    if response.status_code == 200:
        return True, response_body

    if response.status_code == 201:
        return True, response_body

    if response.status_code == 203:
        return True, response_body

    if response.status_code == 204:
        return True, response_body

    if response.status_code == 302:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            if response_body["status"]["statusCode"] == "ERROR_SYNTAX":
                raise SyntaxError(error_message)
            else:
                raise ValueError(error_message)
        else:
            raise ValueError("Unknown message in 400 HTTP CODE")

    if response.status_code == 401:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise ConnectionError(error_message)

    if response.status_code == 403:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise PermissionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 408:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise TimeoutError(error_message)

    if response.status_code == 500:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise SystemError(error_message)

    if response.status_code == 503:
        validation, error_message = validate_payu_response_body_when_error(response_body)
        if validation:
            raise BrokenPipeError(error_message)

    return False, response_body


def validate_payu_response_body_when_error(response_body: dict) -> (bool, str):
    if "status" in response_body and "statusCode" in response_body["status"]:
        error_message = [response_body["status"]["statusCode"]]
        code_literal = response_body["status"]["codeLiteral"] if "codeLiteral" in response_body["status"] else ""
        if code_literal != "":
            error_message.append(code_literal)
        status_desc = response_body["status"]["statusDesc"] if "statusDesc" in response_body["status"] else ""
        if status_desc != "":
            error_message.append(status_desc)
        return True, " | ".join(error_message)
    return False, ""


def validate_payu_auth_success(response_body: dict) -> bool:
    if (
        "access_token" in response_body
        and "token_type" in response_body
        and "expires_in" in response_body
        and "grant_type" in response_body
    ):
        return True
    return False


def validate_payu_create_order_success(response_body: dict) -> (bool, str, str):
    if (
        "status" in response_body
        and "statusCode" in response_body["status"]
        and response_body["status"]["statusCode"] in ["SUCCESS", "WARNING_CONTINUE_3DS"]
        and "orderId" in response_body
    ):
        return True, response_body.get("orderId", None), response_body.get("redirectUri", None)

    return False, "", ""


def validate_payu_get_payment(response_body: dict) -> (bool, str, str):
    if (
        "status" in response_body
        and "statusCode" in response_body["status"]
        and response_body["status"]["statusCode"] in ["SUCCESS", "WARNING_CONTINUE_3DS"]
    ):
        return True, response_body
    return False, ""

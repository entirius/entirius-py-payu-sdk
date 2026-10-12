# entirius-py-payu-sdk

A Python client for the PayU payment gateway REST API, part of Entirius, the open-source modular ecommerce platform.
It wraps OAuth authorization, order creation, payment lookup and card token operations behind one `PayU` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-payu-sdk.svg)](https://pypi.org/project/entirius-py-payu-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-payu-sdk.svg)](https://pypi.org/project/entirius-py-payu-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-payu-sdk/blob/develop/LICENSE)

## What it does

- Authorizes against PayU with OAuth client credentials (`authorize()`).
- Creates orders from typed request DTOs (`create_order()`).
- Reads the payment state of an order (`get_payment()`).
- Adds and deletes stored card tokens (`add_card()`, `delete_card()`).
- Switches between the production and the sandbox API with one call (`use_sandbox()`).

## Installation

```shell
uv add entirius-py-payu-sdk
pip install entirius-py-payu-sdk
```

The import name is `payu_sdk`.

## Quick start

```python
from payu_sdk import PayU

payu = PayU(client_id="...", client_secret="...", pos_id="...")
payu.use_sandbox(True)
payu.authorize()
```

## Requirements

- Python 3.11 or newer.
- `requests` (installed as a dependency).
- A PayU merchant account (client id, client secret, POS id); a sandbox account for testing.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-payu-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is one of the payment gateway clients used by the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Checkout module: https://github.com/entirius/entirius-django-checkout
- Sibling gateway SDKs: https://github.com/entirius/entirius-py-paynow-sdk, https://github.com/entirius/entirius-py-przelewy24-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest); the integration test is skipped without PAYU_SANDBOX_* env vars
```

Development and agent instructions: https://github.com/entirius/entirius-py-payu-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-payu-sdk/blob/develop/LICENSE.

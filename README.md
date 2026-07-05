# payu-sdk

PayU payment gateway SDK — authorization, orders, and card operations over the PayU REST API.

## Installation

```shell
pip install entirius-py-payu-sdk
```

## Usage

```python
from payu_sdk import PayU

payu = PayU(client_id="...", client_secret="...", pos_id="...")
payu.use_sandbox(True)
payu.authorize()
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest) — integration test skipped without PAYU_SANDBOX_* env vars
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).

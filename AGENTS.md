# AGENTS.md

PayU payment gateway SDK — distribution `entirius-py-payu-sdk`, import `payu_sdk`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `payu_sdk` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`src/payu_sdk/`: `payu_sdk.py` holds the `PayU` client (OAuth authorize, orders, payment lookup, card add/delete)
over the PayU REST API; request DTOs live in `dto/`, response checks in `validators/`. Runtime dependency: `requests`.
The integration test hits the PayU sandbox and is skipped without `PAYU_SANDBOX_*` env vars.

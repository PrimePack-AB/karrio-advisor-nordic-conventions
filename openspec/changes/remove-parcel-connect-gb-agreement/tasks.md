# Tasks

## 1. Territory reading

- [x] 1.1 Add an invoice copy test for a 233 shipment to `IM` with postal code IM1 1AA stating the 650 kr Great Britain fee; verify it passes before the advisory is removed.

## 2. Removal

- [x] 2.1 Remove `parcel_connect_gb_agreement` from `codes.py`, `rules/dhl_freight_sweden.py`, `procedures.RULES`, and `procedures.ANSWERING`; remove `DHL_MAN_PARCEL_CONNECT_COUNTRIES`, `DHL_CONNECTOR_SANDBOX_112_GB_REJECTED`, and `DHL_CONNECTOR_REJECTION_112_GB_URL` from `sources.py`; remove the tests that exercise only the advisory and drop it from the tests that iterate over advisors.
- [x] 2.2 In the same commit, remove the advisory's row, Codes list line, and `dhl-connector-gb-rejection` footnote from `docs/concepts/advisories.md`, and its "Great Britain by agreement only" cells from the README matrix.

## 3. Verification and archive

- [x] 3.1 Run `.venv/bin/python -m unittest discover -s tests`, `pyright`, the parity suite with `PYTHONPATH=../karrio-dhl-freight-sweden`, and the four `AGENTS.md` verification commands.
- [x] 3.2 Run `openspec validate remove-parcel-connect-gb-agreement --strict`; verify it is valid, then archive the change.

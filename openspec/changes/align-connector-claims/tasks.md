# Tasks

## 1. Gates before apply

- [x] 1.1 Resolve design.md's three open questions with the user, and if an answer differs from the design's default, revise the artifacts with the openspec-update-change workflow before any code edit; verify `openspec validate align-connector-claims --strict` passes afterwards.
- [x] 1.2 Re-run the PostNord claim audit of `.claude/skills/connector-sync/SKILL.md` immediately before apply, against karrio-postnord `origin/main`; if it has moved past b03ddd0c037a935f50b38727c8e15c479cda303f, diff `README.md`, `karrio/providers/postnord/units.py`, `karrio/providers/postnord/shipment/create.py`, and `karrio/mappers/postnord/proxy.py` from b03ddd0 to the new commit, and stop and update this change if `customs_structure`, `_customs_declaration_cn23`, the standalone customs document fetch, the `customsInvoice` type mapping, or README L157-L212 changed; record the audited commit in the apply notes.
- [x] 1.3 Run the DHL Freight Sweden claim audit the same way against karrio-dhl-freight-sweden `origin/main`, checking that `CommercialInvoiceRequiredError`, `_check_commercial_invoice`, `_customs_services`, and the `voecSupplyVAT` mapping still behave as design.md cites them at c87894125c9c1aebcd74095bd24a68c9eb098cdc and that the README sections "Customs services" and "Commercial or proforma invoice" still state them; stop and update this change on any difference.

## 2. Sources

- [x] 2.1 In `karrio/plugins/advisor_nordic_conventions/sources.py`, add `PN_CONNECTOR_README_URL` and `DHL_CONNECTOR_COMMERCIAL_INVOICE_CHECK` with the URLs and annotations design.md gives, using the commit audited in task 1.2 if it differs from b03ddd0 only in files the audit found unchanged.
- [x] 2.2 Replace `PNS_PARCEL_CUSTOMS_INVOICE`, `PNS_INTERNATIONAL_PARCEL_CN22`, `PNS_COMMERCIAL_FLAG`, `DFS_CUSTOMS_SERVICES_OPT_IN`, `DFS_VOEC_SERVICE`, and `DFS_COMMERCIAL_FLAG` with `PN_CONNECTOR_PARCEL_CUSTOMS_INVOICE`, `PN_CONNECTOR_INTERNATIONAL_PARCEL_CN23`, `PN_CONNECTOR_COMMERCIAL_FLAG`, `DHL_CONNECTOR_CUSTOMS_SERVICES_OPT_IN`, `DHL_CONNECTOR_VOEC_SERVICE`, `DHL_CONNECTOR_COMMERCIAL_FLAG`, and add `DHL_CONNECTOR_COMMERCIAL_INVOICE_REQUIRED`, each tagged S with the locator and verbatim statement of design.md's citation table; remove `CONNECTOR_FLAG_MAPPING`, `PNS`, and `DFS`; keep `FACTS_NOTE`; verify `sources.ALL`, which collects the module's `Source` objects, holds the new ones and not the removed ones.
- [x] 2.3 Rewrite the `sources.py` module docstring so it names the connector commits instead of the fork's PNS and DFS specs, keeping the FN tag convention; update the references in `rules/postnord.py`, `rules/dhl_freight_sweden.py`, `rules/invoice_type.py`, `attestations.py`, `tests/advisor_nordic_conventions/test_postnord.py`, `test_attestations.py`, and `test_dhl_freight_sweden.py` to the new names; verify `rg -n 'PNS|DFS|CONNECTOR_FLAG_MAPPING' karrio tests` prints nothing and `test_sources.py` passes.
- [x] 2.4 In the same commit, in `docs/concepts/advisories.md`, change the Sources cells of Digital invoice to Norway, Postpaket Utrikes invoice, Customs mode missing, VOEC marking, Invoice type mismatch, and Attestation conflict as design.md's Documentation section states; remove the `[^pns]` and `[^dfs]` footnotes and add `[^pn-connector-readme]` and `[^dhl-connector-commercial-invoice-check]`, each repeating its constant's URL and annotation verbatim and ending with the constant name in backticks, as AGENTS.md requires; verify the four AGENTS.md verification commands print nothing.

## 3. Postpaket Utrikes message

- [x] 3.1 Test-first: change the expected connector sentence in `tests/advisor_nordic_conventions/test_postnord.py` to design.md's message for both the Norway and the other destinations text, and the expected `details` source to `PN_CONNECTOR_INTERNATIONAL_PARCEL_CN23`; watch the tests fail, then change `connector_note` in `rules/postnord.py`; verify `test_postnord.py` passes.
- [x] 3.2 In the same commit, in `README.md`, replace "(supply yourself)" with "(supply the invoice; check the printed CN23)" in both cells of the "PostNord SE 91, commercial" matrix row, keeping their links; check the Postpaket Utrikes invoice row of `docs/concepts/advisories.md`, whose Level, Destinations, and Trigger cells stay unchanged; verify the four AGENTS.md verification commands print nothing and `test_doc_links.py` passes.
- [x] 3.3 Verify against the audited karrio-postnord commit that a `postnord_postpaket_utrikes` booking from SE to US with customs commodities produces `customsDeclarationCN23` and no `customsInvoice`, by running the connector's own International Parcel customs tests in `connectors/postnord` with the development interpreter; record the test names and result in the apply notes.

## 4. Invoice type message

- [x] 4.1 Test-first: in `tests/advisor_nordic_conventions/test_invoice_type.py`, expect the DHL Freight Sweden warning to state the `CommercialInvoiceRequiredError` refusal with design.md's text, the PostNord warning to keep the proforma statement, and the per-carrier `details` sources of design.md's table; watch them fail, then split the warning text by carrier in `rules/invoice_type.py` and update `CARRIER_SOURCES`; verify `test_invoice_type.py` passes and the `info` branch is unchanged for both carriers.
- [x] 4.2 In the same commit, check the Invoice type mismatch row of `docs/concepts/advisories.md` and the Both carriers summary line of `README.md` against the new messages; the row's Level, Destinations, and Trigger cells stay unchanged; verify the four AGENTS.md verification commands print nothing.
- [x] 4.3 Verify against the audited karrio-dhl-freight-sweden commit that a sale-like booking from SE to NO without `customs.commercial_invoice` raises `CommercialInvoiceRequiredError`, by running the connector's own test for it in `connectors/dhl-freight-sweden`; record the test name and result in the apply notes.

## 5. Service-set comment and specification Purpose

- [x] 5.1 Replace the comment at `karrio/plugins/advisor_nordic_conventions/lanes.py:25` with the karrio-postnord commit and `units.py` L157-L168 and L318-L334 of design.md's table; verify `test_lanes.py` passes, including the connector cross-check, and that it does not skip.
- [x] 5.2 Edit `openspec/specs/plugins/advisor-nordic-conventions/spec.md` directly, because deltas ignore `## Purpose`: replace the PNS and DFS sentence, the `feat-postnord-customs-invoice` sentence, the "as defined by PNS lines 10-11" clause, the karrio `develop` 7a56ffa5b `units.py:269-284` citation, and, per decision 3, the fork live-verification note citation with the connector permalinks of design.md's table, keeping the FN sentence; verify `rg -n 'PNS|DFS|7a56ffa5b|feat-postnord-customs-invoice' openspec/specs` prints nothing after archive.

## 6. Connector sync

- [x] 6.1 Run `.venv/bin/python -m unittest discover -s tests` and the pytest run of the connector-sync skill with both connectors checked out at the audited commits; verify every test passes and no connector cross-check test skips.
- [x] 6.2 Run the connector-sync skill for PostNord, then for DHL Freight Sweden, so it bumps `connectors/postnord` and `connectors/dhl-freight-sweden` to the audited commits and advances the reading pins whose cited content is unchanged, `PN_CONNECTOR_README_URL`, `DHL_CONNECTOR_README_URL`, and the `lanes.py` comment among them, each with its footnote; verify each run ends in its `chore(connectors): sync <c> to <short-sha>` commit and reports no stale claim.
- [x] 6.3 Update the "Out of scope, reported only" list in `.claude/skills/connector-sync/SKILL.md` and the fork pin entries of its `reference.md` so it names only the fork pins left after this change (`FACTS_NOTE` and the FN locators), on this branch after its rebase onto `connector-sync-skill`, per decision 4; verify `rg -n 'PNS|DFS|CONNECTOR_FLAG_MAPPING' .claude/skills/connector-sync` prints nothing.

## 7. Verification and archive

- [ ] 7.1 Re-run the PostNord claim audit of task 1.2 immediately before archive against karrio-postnord `origin/main`; if it moved and a cited behaviour changed, stop and update this change instead of archiving.
- [ ] 7.2 Run the four AGENTS.md verification commands, `.venv/bin/python -m unittest discover -s tests`, and `pyright`; verify all pass.
- [ ] 7.3 Run `openspec validate align-connector-claims --strict`; verify it is valid, then archive the change.

## Apply notes

Tasks 1.2 and 1.3, 2026-10-19: `origin/main` of karrio-postnord is b03ddd0c037a935f50b38727c8e15c479cda303f and of karrio-dhl-freight-sweden is c87894125c9c1aebcd74095bd24a68c9eb098cdc, the commits this change cites, so the audited commits are these and no diff past them exists.
At these commits `customs_structure`, `_customs_declaration_cn23`, the proxy's standalone customs document fetch, the `customsInvoice` type mapping, README L157-L212, `CommercialInvoiceRequiredError`, `_check_commercial_invoice`, `_customs_services` with its `voecSupplyVAT` mapping, and the README sections "Customs services" and "Commercial or proforma invoice" read as design.md cites them.
The pytest run with both connectors checked out at these commits passes except `test_territories.py::...test_matches_connector_tables[postnord]`, the EU VAT area table mismatch this change leaves out of scope, and no connector cross-check test skips.

Task 3.3: in `connectors/postnord` at b03ddd0, the connector's tests selected by `-k 'cn23 or international_parcel'` in `tests/postnord/test_shipment.py`, among them `test_create_shipment_cn23_request`, which asserts `customsDeclarationCN23` and no `customsInvoice` or `customsDeclarationCN22` for a `postnord_postpaket_utrikes` booking from SE to NO, pass 13 of 16.
The three failures, `test_international_parcel_labels_are_not_composition_verified` (two cases) and `test_international_parcel_label_without_cn22_format_is_not_verified`, assert an empty message list and receive this plugin's own `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` advisory, because the development environment's karrio loads the installed advisor plugin during the connector's shipment parse; they do not bear on the CN23 claim.
The same request mapped with the recipient changed to US 10001 carries `customsDeclarationCN23` and neither `customsInvoice` nor `customsDeclarationCN22`.

Task 4.3: in `connectors/dhl-freight-sweden` at c878941, `tests/dhl_freight_sweden/test_shipment.py::TestDHLFreightShipment::test_shipment_sale_without_commercial_invoice_surfaces_field_error` passes; its four cases book 202 from SE to NO with sale-like content and `customs.commercial_invoice` false or unset, and receive a `SHIPPING_SDK_FIELD_ERROR` on `customs.commercial_invoice` without a request being sent.
Mapping its `ShipmentPayload202MerchandiseNoFlag` directly raises `CommercialInvoiceRequiredError`.

Task 5.1: the `lanes.py` comment cites karrio-postnord b03ddd0 `units.py` L154-L168 and L318-L334 rather than design.md's L157-L168, because the code `91` that `POSTNORD_INTERNATIONAL_PARCEL` mirrors is at L154.
Task 5.2: before archive, `rg -n 'PNS|DFS|7a56ffa5b|feat-postnord-customs-invoice' openspec/specs` still prints lines in the requirements this change's delta replaces; the Purpose section prints none.

Task 6.1: with `connectors/postnord` at b03ddd0 and `connectors/dhl-freight-sweden` at c878941, `unittest discover -s tests` runs 267 tests with no failure, and pytest passes 267 with 272 subtests; no connector cross-check test skips.
The PostNord EU VAT area table mismatch the proposal leaves out of scope is encoded in `test_territories.py` as `KNOWN_MISSING_CONNECTOR_RANGES`: for PostNord, `test_matches_connector_tables` asserts that the connector's `NON_EU_VAT_POSTAL_RANGES` equals the plugin's table without exactly FR 97000-97999, DK 3800-3999, FR 98600-98899, and EL 63086, so any other divergence, or the connector adding those ranges, fails the test with a message to remove the expectation, while the DHL Freight Sweden case still asserts full equality.
The connector-sync skill now reports such an encoded difference as a known finding that does not block the bump.

Task 6.2: `connectors/dhl-freight-sweden` is synced to c878941 in `chore(connectors): sync dhl-freight-sweden to c878941`, advancing the `units.py` reading comments in `lanes.py`, `exclusions.py`, and `rules/dhl_country_requirements.py`, whose mirrored constants are unchanged; `DHL_CONNECTOR_README_URL` and `DHL_CONNECTOR_DESTINATIONS_URL` stay at 7a2214d, because the cited README sections "Customs services" and "Commercial or proforma invoice" and the destinations sections "Åland" and "Excluded postal codes" changed while the claims still hold.
`connectors/postnord` is synced from 3899da8 to b03ddd0 in `chore(connectors): sync postnord to b03ddd0`; no reading pin moves, because `PN_CONNECTOR_README_URL`, its footnote, the `sources.py` module docstring, and the `lanes.py` service-set comment already cite b03ddd0.

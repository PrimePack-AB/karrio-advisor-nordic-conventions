# Proposal

## Why

Two advisory messages state what a connector does, and neither statement holds for the standalone connectors the plugin runs against.
`advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` says the PostNord connector "currently sends CN22 declaration data and no invoice for International Parcel", but karrio-postnord books a CN23 for International Parcel (91) unconditionally (`customs_structure`, karrio-postnord `units.py` L431-L439 at b03ddd0, S), and did so already at the pinned gitlink 3899da8.
`advisor_nordic_conventions_invoice_type_content_mismatch` says "The connector declares a proforma invoice because customs.commercial_invoice is not true", but since karrio-dhl-freight-sweden ec180e6 (committed 2026-10-06) the DHL Freight Sweden connector refuses a sale-like booking across the EU VAT area border without `customs.commercial_invoice` true, with `CommercialInvoiceRequiredError`, and drops customs data inside the area (S, `shipment/create.py` L513-L516 and L1062-L1090 at c878941), so it never declares that proforma invoice.
Both claims are already stale at the pinned gitlinks 3899da8 and 62c1f46, so the connector-sync procedure cannot bump either submodule until the specification changes.

The connector-behaviour sources that back these and four other advisories, `PNS`, `DFS`, and the `CONNECTOR_FLAG_MAPPING` path, cite the karrio fork's specs and code at 60312fe2e, and `lanes.py` cites the fork's PostNord service sets at `develop` 7a56ffa5b.
The standalone connectors now publish the same behaviour in their README and `docs/concepts/` pages and code, which are the documents the plugin's users can read and the commits the connector-sync audit checks.

The PostNord connector is under active development on the Print API and on customs correctness, and its README opens with "This project is actively in development, expect breaking changes." (karrio-postnord b03ddd0, `README.md` L3-L4, S).
The re-stated PostNord claim is therefore pinned to a cited connector commit, and the PostNord connector-sync audit is re-run immediately before apply and again before archive.

## What Changes

- The Postpaket Utrikes invoice advisory states that the PostNord connector sends CN23 declaration data and no invoice for International Parcel, citing karrio-postnord at b03ddd0, that the standalone CN23 is attached only with the `postnord_standalone_customs_documents` option set, and that the consumer supplies the invoice and the printed CN23; the level, trigger, destinations, copy counts, and Norway routes are unchanged.
- The recorded gap "PostNord requires the CN23 for International Parcel at every value … while the connector sends CN22 declaration data for it" is narrowed: the connector now books the CN23 data at every value when the booking carries customs commodities, and what remains unadvised is the printed CN23 for non-commercial International Parcel, whose composition into the label is unverified.
- The invoice type advisory keeps its trigger and levels; its warning for a DHL Freight Sweden booking states that the connector refuses the booking with `CommercialInvoiceRequiredError`, and its warning for a PostNord parcel product keeps the proforma statement, which karrio-postnord b03ddd0 still implements (`shipment/create.py` L706-L710, S).
- `PNS`, `DFS`, the `PNS_*` and `DFS_*` sources, `CONNECTOR_FLAG_MAPPING`, and the `lanes.py` service-set comment are re-pointed to karrio-postnord at b03ddd0 and karrio-dhl-freight-sweden at 7a2214d and c878941, as design.md's citation table lists; `FACTS_NOTE` keeps its fork citation, because neither connector carries an equivalent.
- The `PNS` and `DFS` footnotes in `docs/concepts/advisories.md` give way to footnotes for the new connector document constants, and the README matrix cells and Sources cells follow the new message text and citations.
- Once both claims hold, the connector-sync skill bumps `connectors/postnord` and `connectors/dhl-freight-sweden` to the audited commits.

No advisory code, level, trigger, destination, or answering set changes; only message text, `details` sources, and citations change.

Out of scope, recorded as follow-ups:

- The EU VAT area tables disagree: the plugin treats FR 97000-97999, DK 3800-3999, FR 98600-98899, and EL 63086 as outside the EU VAT area, while karrio-postnord's `NON_EU_VAT_POSTAL_RANGES` (b03ddd0, `units.py` L350-L361) omits them; this is likely a connector-side customs-correctness issue to raise with the PostNord work, in a separate change.
- New DHL Freight Sweden behaviour without an advisory: the service point counted as a delivery address in the EU VAT area test and in the Åland refusals, the default `ProductNotOfferedError` refusing 109 and 112 to Great Britain together with the `separate_agreement_lane` warning, `InternationalAccountNumberError` for 202, 205, 233, SPI, and 601, and the pickups API.
- karrio-postnord's own documents disagree on the International Parcel CN23: `README.md` L78 calls the opt-in's document "the standalone CN22 of letter and International Parcel (91) bookings", and `docs/notes/integration/customs-at-booking.md` L88 says the declaration is composed into `docs.label` by default, while `shipment/create.py` L29-L32 says the CN23 composition is a pending live verification; this is reported to the PostNord work, not resolved here.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugins/advisor-nordic-conventions`: modifies "PostNord Sweden commercial Postpaket Utrikes carries a commercial invoice" and "The invoice type matches the content type" in substance, and re-points the connector citations of "PostNord Sweden to Norway invoices go digitally", "DHL Freight Sweden needs a customs handling mode", "DHL Freight Sweden VOEC ID is marked on the package", and "Contradicted attestations are reported"; the Purpose section's connector source paragraph is edited directly.

## Impact

`rules/postnord.py`, `rules/invoice_type.py`, `sources.py`, `attestations.py` (source name only), the comment in `lanes.py`, tests, `README.md`, `docs/concepts/advisories.md`, the main specification, and the `connectors/postnord` and `connectors/dhl-freight-sweden` gitlinks.
Advisory codes, levels, and attestations are public API and do not change; two advisory messages change wording.

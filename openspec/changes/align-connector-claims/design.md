# Design

## Context

The plugin runs against the standalone connectors karrio-postnord and karrio-dhl-freight-sweden, and its development-only submodules pin the connector commits last audited against its claims: `connectors/postnord` at 3899da8 and `connectors/dhl-freight-sweden` at 62c1f46.
The audit targets are the connectors' `origin/main` commits read on 2026-10-19: karrio-postnord b03ddd0c037a935f50b38727c8e15c479cda303f (committed 2026-10-14) and karrio-dhl-freight-sweden c87894125c9c1aebcd74095bd24a68c9eb098cdc (committed 2026-10-19).
Both pinned commits are ancestors of these targets.
All connector evidence below is tagged S and cited by permalink at those commits, abbreviated as follows.

- PN: `https://github.com/PrimePack-AB/karrio-postnord/blob/b03ddd0c037a935f50b38727c8e15c479cda303f/`
- DHL: `https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/blob/c87894125c9c1aebcd74095bd24a68c9eb098cdc/`
- DHL-README-pin: `https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/blob/7a2214d26c0a8afef6e0bc3a4c4991c9e367988f/README.md`, the reading pin `DHL_CONNECTOR_README_URL` already holds (read 2026-10-08)

## PostNord International Parcel

The connector selects the booking's customs structure by service code, and International Parcel (91) takes `customsDeclarationCN23` (PN `karrio/providers/postnord/units.py#L431-L439`, `customs_structure`).
The CN23 is built from the CN22 row mapping and checks, minus `countryOfOrigin`, with `postalCharges` booked as zero (PN `karrio/providers/postnord/shipment/create.py#L518-L571`, `_customs_declaration_cn23`).
The CN23 type carries no invoice number, invoice date, or invoice type, and the connector builds a `customsInvoice` only for the parcel-product structure (PN `karrio/providers/postnord/shipment/create.py#L890-L903`), so a 91 booking carries no invoice.
The README states it in prose: "International Parcel (91) sends a CN23 declaration (`customsDeclarationCN23`)", "International Parcel (91) books the CN23 unconditionally", and "Duties after booking, such as printing the customs documents and attaching the invoice copies to the parcel, are the consumer's." (PN `README.md#L160-L162`).

Whether the consumer gets a printed CN23 from the booking is open.
"whether PostNord composes the CN23 into the label is a pending live verification" (PN `karrio/providers/postnord/shipment/create.py#L29-L32`), and the README says "a phase-2 sandbox capture of a CN23 booking decides whether PostNord composes a CN23 into the label and what its stamping needs, so until then 91 bookings' documents pass through unverified" (PN `README.md#L209`).
The standalone CN23 is fetched only "if the `postnord_standalone_customs_documents` opt-in is set" (PN `README.md#L212`; PN `karrio/mappers/postnord/proxy.py#L154-L178`), and the option defaults to false (PN `karrio/providers/postnord/units.py#L74-L76`).

The connector built a CN23 for 91 already at 3899da8, its first standalone commit, so the advisory's CN22 claim was stale when the submodule was added.

### Message

The connector sentence of `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` becomes, for both the Norway and the other destinations text:

> The connector currently sends CN23 declaration data and no invoice for International Parcel; it returns the CN23 as a separate document only when postnord_standalone_customs_documents is set, and whether PostNord prints the CN23 on the label is unverified, so supply the invoice yourself and check that the printed CN23 travels with the parcel.

The sentence keeps "currently", as every other connector claim in the plugin does, and the commit it rests on travels in `details` through the cited source, whose reference is the README permalink at b03ddd0.
The specification states the claim "as of karrio-postnord b03ddd0", so a later connector commit that changes the behaviour is a stale claim the connector-sync audit reports against a named commit.
Putting the sha into the user-facing message was considered and not chosen, because no other advisory message carries a commit and the message would change on every re-audit; decision 1 records the user's confirmation.

The sentence describes a booking whose customs data carries at least one commodity; with customs data and no commodity the connector sends no customs structure at all.
The advisory's trigger, `commercial`, does not look at commodities, and the current sentence has the same imprecision, so the trigger is left unchanged.

### Recorded gaps

The gap in "PostNord Sweden commercial Postpaket Utrikes carries a commercial invoice" said the connector sends CN22 data for 91 although PostNord requires the CN23 at every value.
The data half is closed: the connector books the CN23 for 91 at every value, commercial or not, whenever the booking carries customs commodities outside the EU VAT area.
The gap that remains is the printed CN23 for non-commercial International Parcel: no advisory tells the consumer to make sure it travels with the parcel, while its composition into the label is unverified and the standalone CN23 is opt-in.

The gap in "The invoice type matches the content type" said the connector drops `customs.commercial_invoice`, `customs.invoice`, and `customs.invoice_date` for International Parcel and letter services.
It still holds at b03ddd0, with CN23 in place of CN22 for 91, and its citation moves from the fork's `feat-postnord-customs-invoice` at 1b40eeb7e to PN `karrio/providers/postnord/shipment/create.py#L518-L571` and `#L890-L903`.

## Invoice type

### DHL Freight Sweden

karrio-dhl-freight-sweden ec180e6 ("feat: refuse sale-like exports without a commercial invoice", committed 2026-10-06) added `CommercialInvoiceRequiredError` (DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L160-L163`).
Across the EU VAT area border, a booking with customs data whose content is sale-like and whose `customs.commercial_invoice` is not true is refused before it is sent (DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L513-L516` and `#L1062-L1090`), and inside the area customs data is dropped with a `customs_omitted_intra_eu` warning (DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L489-L506`).
The connector's sale-like test excludes `documents`, `gift`, `return_merchandise`, and `sample`, the same set as the plugin's `lanes.NOT_SALE_LIKE_CONTENT` (DHL `karrio/providers/dhl_freight_sweden/units.py#L116-L137`).
The README at the existing reading pin already states it: "Outside the EU VAT area, content counts as a sale unless `customs.content_type` is `documents`, `gift`, `return_merchandise`, or `sample`, and a sale without `customs.commercial_invoice` true fails with `CommercialInvoiceRequiredError`." (DHL-README-pin L349), and ec180e6 is an ancestor of 7a2214d and of the pinned 62c1f46.

The warning's statement that the connector declares a proforma invoice therefore never holds on a DHL Freight Sweden booking the advisory covers.
The advisory is kept and its DHL warning states the refusal, as the plugin already does for the Åland customs service, the joint declaration destination, and the territory postal code, which warn before the connector refuses.
Removing the DHL warning, as `remove-parcel-connect-gb-agreement` removed an advisory the connector covered, was considered; that removal rested on false warnings to shippers holding an agreement, which does not apply here, because the plugin's and the connector's conditions coincide.
Decision 2 records the user's confirmation.

The DHL warning message becomes:

> The connector refuses this booking with CommercialInvoiceRequiredError because customs.commercial_invoice is not true but the content is described as goods for sale. A proforma invoice is for gifts and samples for which the recipient makes no payment; set commercial_invoice to true for goods sold.

When the customs data carries no commodity, invoice number, or invoice date, the connector refuses earlier with `CustomsInformationRequiredError` (DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L507-L508`), so the named error is the one a booking with customs content receives; this imprecision is accepted.
The `info` message for a commercial invoice declared for a gift or sample stays as it is, because the connector books it (DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L696-L702`).

### PostNord

At b03ddd0 the parcel-product customs invoice still takes its type literally from the flag: "`customs.commercial_invoice` | `type`: `COMMERCIAL` when true, `PROFORMA` when false or omitted" (PN `README.md#L187`; PN `karrio/providers/postnord/shipment/create.py#L706-L710`), and the connector has no sale-like check.
The PostNord warning keeps its current message, and `PNS_COMMERCIAL_FLAG` is re-pointed without its clause "mismatch detection is left to advisory tooling", which only the fork spec states (PNS line 158).

## Citation re-pointing

New and changed document constants, each annotated with its read date as the other connector constants are:

- `PN_CONNECTOR_README_URL`: PN `README.md` (read 2026-10-19), new, with the footnote `[^pn-connector-readme]` "PostNord connector README".
- `DHL_CONNECTOR_COMMERCIAL_INVOICE_CHECK`: `https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/ec180e61ca7ae4e763f58d9919ad9be0ae2ab56f (committed 2026-10-06)`, new, a historical-event citation like `DHL_CONNECTOR_TERRITORY_CHECK`, with the footnote `[^dhl-connector-commercial-invoice-check]` "DHL connector commercial invoice check".
- `DHL_CONNECTOR_README_URL` is reused at its pin 7a2214d, whose "Customs services" and "Commercial or proforma invoice" sections state every DFS claim; advancing it to c878941 is left to the connector-sync bump.
- `PNS` and `DFS` are removed with their footnotes once no source cites them.

| Citation | Where | Current | Replacement |
|---|---|---|---|
| `FACTS_NOTE` | `sources.py:21`, cited by `PN_SE_PLASTIC_POCKET_ORIGIN`, `PN_FI_GOVERNING_UNRESOLVED`, `DHL_OWN_DECLARATION_FEE_INFERENCE`, `DHL_OUTSIDE_COPIES_UNCONFIRMED` (all I) | fork `docs/notes/customs/nordic-trade-documents-facts.md` at baf8eb3dd | No equivalent; keep the fork citation. The note records carrier and authority documents and inferences over them, not connector behaviour, and neither connector ports it: karrio-postnord's printout note still cites it as a fork note (PN `docs/notes/sandbox/booking-printout-composition-verification.md#L33`), and the DHL README restates the manual's outside copies for 109 only (DHL `README.md#L382`), not the 112 and road-freight inference. Inference-only sources are not listed in Sources cells, so no footnote changes. The FN line locators of W sources keep pointing into the note. |
| `PNS` | `sources.py:22` | fork `openspec/specs/postnord/customs-declaration/spec.md` at 60312fe2e | Removed; its sources cite `PN_CONNECTOR_README_URL`. |
| `PNS_PARCEL_CUSTOMS_INVOICE` | `sources.py:113-120`; `rules/postnord.py:98`, `attestations.py:59` | PNS:28-31, implemented at face88f37 and 52d21fbfb | `PN_CONNECTOR_PARCEL_CUSTOMS_INVOICE`, S, locator "Customs declarations, At booking": "When a shipment carries `customs` with at least one commodity, the booking embeds one customs structure selected by the service." and "every other service is a parcel product and sends a customs invoice (`customsInvoice`)" (PN `README.md#L157`, `#L160`); code PN `karrio/providers/postnord/units.py#L431-L439`. |
| `PNS_INTERNATIONAL_PARCEL_CN22` | `sources.py:121-125`; `rules/postnord.py:147` | PNS:10, PNS:13-16 | `PN_CONNECTOR_INTERNATIONAL_PARCEL_CN23`, S, locators "Customs declarations" and "Standalone customs documents": PN `README.md#L160-L162`, `#L209`, `#L212`, quoted above; code PN `karrio/providers/postnord/units.py#L431-L439`, `shipment/create.py#L518-L571`, `#L29-L32`. |
| `PNS_COMMERCIAL_FLAG` | `sources.py:308-312`; `rules/invoice_type.py:19` | PNS:155-168 | `PN_CONNECTOR_COMMERCIAL_FLAG`, S, locator "Customs invoice mapping": PN `README.md#L187`, quoted above; code PN `karrio/providers/postnord/shipment/create.py#L706-L710`. The advisory-tooling clause is dropped. |
| `DFS` | `sources.py:23` | fork `openspec/specs/dhl-freight-sweden/customs/spec.md` at 60312fe2e | Removed; its sources cite `DHL_CONNECTOR_README_URL`. |
| `DFS_CUSTOMS_SERVICES_OPT_IN` | `sources.py:190-194`; `rules/dhl_freight_sweden.py:95` | DFS:75-83 | `DHL_CONNECTOR_CUSTOMS_SERVICES_OPT_IN`, S, locator "Customs services": "The manual offers four customs services, and the connector sends none unless an option selects it; each carries a DHL fee, and the manual allows only one per shipment." (DHL-README-pin L327; DHL `README.md#L352`); code DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L781-L818`. |
| `DFS_VOEC_SERVICE` | `sources.py:255-259`; `rules/dhl_freight_sweden.py:283` | DFS:66-73 | `DHL_CONNECTOR_VOEC_SERVICE`, S, locator "Customs services": "VOEC (VAT on e-commerce, NO) is sent from `customs.options.voec_number` and has not been booked in the sandbox." (DHL-README-pin L338; DHL `README.md#L363`); code DHL `karrio/providers/dhl_freight_sweden/shipment/create.py#L809-L815`. |
| `DFS_COMMERCIAL_FLAG` | `sources.py:313-317`; `rules/invoice_type.py:25` | DFS:51-64 | `DHL_CONNECTOR_COMMERCIAL_FLAG`, S, locator "Commercial or proforma invoice": "True sends a `CommercialInvoice` document, and false or unset sends a `ProformaInvoice`." and the refusal sentence quoted above (DHL-README-pin L348-L349; DHL `README.md#L374-L375`); and a new `DHL_CONNECTOR_COMMERCIAL_INVOICE_REQUIRED`, S, citing `DHL_CONNECTOR_COMMERCIAL_INVOICE_CHECK` for the refusal's start. |
| `CONNECTOR_FLAG_MAPPING` | `sources.py:323-327`; `rules/invoice_type.py:22`, `:27` | FN:30-36, fork `modules/connectors/dhl_freight_sweden/.../shipment/create.py` | No single-file equivalent: the claim "map it to a commercial versus proforma invoice type, never to producing a document" now differs per connector, since the DHL connector refuses and PostNord composes an invoice document from the `customsInvoice` structure whatever the flag (PN `docs/notes/sandbox/customs-invoice-live-verification.md#L38-L39`). Removed; superseded by `PN_CONNECTOR_COMMERCIAL_FLAG` and `DHL_CONNECTOR_COMMERCIAL_FLAG`. It is not listed in any Sources cell today, so no footnote changes. |
| Comment at `lanes.py:25` | `POSTNORD_LETTER_SERVICES`, `POSTNORD_INTERNATIONAL_PARCEL` | karrio develop 7a56ffa5b, postnord `units.py:264-285` | karrio-postnord b03ddd0 `units.py` L157-L168 (service codes) and L318-L334 (`LETTER_SERVICES`, `INTERNATIONAL_PARCEL_SERVICE`), a reading pin the connector-sync skill advances; the twelve letter codes and 91 match. |
| Specification Purpose, lines 7, 9-12 | main spec | PNS, DFS, the fork branch `feat-postnord-customs-invoice`, karrio `develop` 7a56ffa5b `units.py:269-284`, and the fork note `docs/notes/postnord/customs-declaration-live-verification.md:5` | The connector READMEs and code at the commits above; the live-verification note's ported copy, PN `docs/notes/sandbox/customs-declaration-live-verification.md#L13`, which names UX478114854SE "an SE→PL export letter booked as `postnord_export_letter` (`UX`)". Line 6 (FN) is unchanged. |

The Purpose line 12 citation was found during the audit and is not in the brief; it is included because it is a fork citation with an equivalent, and decision 3 records the user's confirmation.
Renaming the `PNS_*` and `DFS_*` sources is internal: `Source` names are not public API, only their `to_dict()` output in `details`, which changes anyway with the reference.

## Documentation

`docs/concepts/advisories.md` Sources cells change as follows: Digital invoice to Norway, Postpaket Utrikes invoice, and Attestation conflict replace "PostNord connector spec[^pns]" with "PostNord connector README[^pn-connector-readme]"; Customs mode missing drops "DHL connector spec[^dfs]", since "DHL connector README[^dhl-connector-readme]" is already listed; VOEC marking replaces it with "DHL connector README[^dhl-connector-readme]"; Invoice type mismatch replaces both connector specs with "PostNord connector README[^pn-connector-readme], DHL connector README[^dhl-connector-readme], DHL connector commercial invoice check[^dhl-connector-commercial-invoice-check]".
No Level, Destinations, or Trigger cell changes.
The README matrix row "PostNord SE 91, commercial" keeps its links and replaces "(supply yourself)" with "(supply the invoice; check the printed CN23)" in both columns, and the Both carriers summary line keeps "goods sold need a commercial invoice, not a proforma".
The `sources.py` module docstring and `docs/concepts/advisories.md` line 6 keep the FN tag convention; the docstring's PNS and DFS sentences are replaced by the connector commits.

## Risks

The PostNord connector is under active development on the Print API and customs correctness, and its README warns of breaking changes (PN `README.md#L3-L4`).
The CN23 claim may go stale again soon, for example when the phase-2 capture settles whether PostNord composes the CN23 into the label, which would change the "unverified" clause.
Mitigation: the claim is pinned to b03ddd0 in the specification and the source reference, the PostNord connector-sync audit runs immediately before apply and again before archive, and a change in `customs_structure`, `_customs_declaration_cn23`, the proxy's standalone fetch, or README L160-L212 between b03ddd0 and the new `origin/main` stops the apply until this change is updated.

karrio-postnord's documents disagree with each other on 91: `README.md#L78` calls the opt-in's document "the standalone CN22 of letter and International Parcel (91) bookings", and `docs/notes/integration/customs-at-booking.md#L88` says declarations are composed into `docs.label` by default, while `shipment/create.py#L29-L32` and `README.md#L209` say the CN23 composition is unverified.
The plugin cites `README.md#L209` and `#L212` and the code, which agree, and reports the disagreement to the PostNord work.

The DHL warning names an error a future connector commit could rename; the DHL connector-sync audit covers it like the other refusal advisories.

## Gitlink bump

The connector-sync skill, run after the claims hold, moves `connectors/postnord` from 3899da8 to the audited karrio-postnord commit and `connectors/dhl-freight-sweden` from 62c1f46 to the audited karrio-dhl-freight-sweden commit, and advances the reading pins whose cited content is unchanged, including `DHL_CONNECTOR_README_URL`, `PN_CONNECTOR_README_URL`, and the `lanes.py` comment.
If either connector's `origin/main` has moved past the commit this design cites, the skill audits the newer commit; a stale claim there stops the bump and returns to this change.

## Decisions

The user approved the following on 2026-10-19, each the design's default.

1. The Postpaket Utrikes message keeps "currently" and names no commit; karrio-postnord b03ddd0c037a935f50b38727c8e15c479cda303f is carried in the advisory `details`, through the cited source's reference, and in the specification only.
2. The DHL Freight Sweden half of the invoice type warning is kept, reworded as a heads-up that the connector refuses the booking with `CommercialInvoiceRequiredError`, consistent with the Åland customs service, joint declaration destination, and territory postal code refusal advisories.
3. The specification Purpose's fork live-verification note citation is re-pointed to the ported PostNord note, PN `docs/notes/sandbox/customs-declaration-live-verification.md#L13`.
4. Task 6.3, the connector-sync skill's out-of-scope list and fork pin entries, is applied on this change's branch after it is rebased onto `connector-sync-skill`, which carries the skill's final text.

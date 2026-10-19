# Spec Delta

## MODIFIED Requirements

### Requirement: PostNord Sweden to Norway invoices go digitally

For a PostNord shipment from Sweden to Norway to which `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` does not apply, the plugin SHALL return code `advisor_nordic_conventions_postnord_se_no_digital_invoice`, stating that PostNord requires the commercial invoice for Norway digitally rather than on paper with the parcel, and naming the routes: the booking itself (the connector transmits a customs invoice for parcel products booked with customs data, S, karrio-postnord `README.md` L157 and L160 at b03ddd0), PostNord Skicka Direkt Business, the email address foravisering.export@postnord.com, and upload in PostNord MyCustoms.
For a Norway-named letter service the message SHALL also state that a commercial invoice and a VOEC number are required for letters to Norway from SEK 0, the invoice sent digitally through the same routes (FN:99, FN:108, W, SV page only); other letter services receive this advisory without that statement.
When `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` applies to a shipment, it carries the Norway invoice routes itself and this advisory SHALL NOT be returned, so each shipment receives the invoice routes once.
The level SHALL be `info` when the booking is a parcel product carrying customs data, because the connector already transmits the invoice data, and `warning` otherwise, because the invoice then reaches PostNord only through a route the consumer owns.
Sources: FN:118 (W, Service Point special terms §4, "To Norway the commercial invoice and shipment list shall be sent digitally"), FN:142 and FN:147 (W, PostNord SE customs documents pages, Norway channels and MyCustoms), FN:149 (W, the separate channels are stated for Norway only), FN:108 (W, SV page, "Vid export till Norge behöver Handelsfaktura och VOEC* anges från 0 kr.").

#### Scenario: Parcel booking with customs data is informational

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_no_digital_invoice` at level `info`, naming Skicka Direkt Business, foravisering.export@postnord.com, and MyCustoms

#### Scenario: Letter to Norway states invoice and VOEC from SEK 0

- **WHEN** a PostNord `postnord_export_letter` shipment from Sweden to Norway is created with customs data whose `content_type` is `merchandise`
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_no_digital_invoice` at level `warning`, stating that a commercial invoice and a VOEC number are required from SEK 0 and that the invoice is sent digitally, and citing the SV page

#### Scenario: Letter not named by the Swedish page omits the SEK 0 statement

- **WHEN** a PostNord `postnord_varubrev_first_class` shipment from Sweden to Norway is created with customs data whose `content_type` is `merchandise`
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_no_digital_invoice` at level `warning` naming the Norway invoice routes, without the commercial invoice and VOEC from SEK 0 statement

#### Scenario: Commercial Postpaket Utrikes to Norway receives the invoice routes once

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to Norway is created with customs data whose `commercial_invoice` is true
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` naming the Norway invoice routes and does not return code `advisor_nordic_conventions_postnord_se_no_digital_invoice`

#### Scenario: Non-commercial Postpaket Utrikes to Norway is a warning

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to Norway is created with customs data whose `content_type` is `gift` and whose `commercial_invoice` is false
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_no_digital_invoice` at level `warning` and not code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice`

### Requirement: PostNord Sweden commercial Postpaket Utrikes carries a commercial invoice

For a commercial PostNord shipment from Sweden to a destination outside the EU VAT area booked as International Parcel (`postnord_postpaket_utrikes`, `91`, "Z91 Postpaket Utrikes" in the connector's vendored general descriptions, FN:165, S; marketed in Denmark as EMS), the plugin SHALL return code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` at level `warning`.
For destinations other than Norway the message SHALL state that the parcel needs the CN23 export declaration and a commercial invoice in three copies with the parcel.
Three copies is the stricter reading of conflicting sources and satisfies both at every value: the Postpaket Utrikes terms §2 require the CN23 in two copies and the commercial invoice in two copies when the value exceeds SEK 2 000 or the goods are sent for commercial purposes (FN:103, FN:111, W), while the EN and SV web pages require a commercial or proforma invoice in triplicate when the value exceeds SEK 2 000, on value only (FN:102, FN:107, FN:109, W); the plugin does not evaluate goods value, and two copies would fall short of the web pages above SEK 2 000.
`details` SHALL list both the terms and the web pages with the copy count and trigger each states.
For Norway the Norway-specific digital-only rule overrides the general copy count: the message SHALL state that the CN23 is required and that the invoice is sent digitally and not attached to the parcel, naming PostNord's Norway routes (the Booking API, PostNord Skicka Direkt Business, foravisering.export@postnord.com, and MyCustoms upload), and `details` SHALL cite the terms, the web pages, and the Norway rule (FN:142, FN:147, W).
The message SHALL state that the connector currently sends CN23 declaration data and no invoice for International Parcel, that it returns the CN23 as a separate document only when `postnord_standalone_customs_documents` is set, that in a test-mode booking PostNord composed the CN23 onto the label and the connector checks PDF labels for it, and that production composition and ZPL labels are unverified, so the consumer must supply the invoice and check that the printed CN23 travels with the parcel; this is the connector's behaviour as of karrio-postnord 320f3ad (S, `README.md` L162-L164, L208, L212, and L219, `units.py` L499-L507, and `shipment/create.py` L29-L38, L123-L148, L194-L240, and L649-L702), and `details` SHALL cite that commit.
Non-commercial Postpaket Utrikes above SEK 2 000 is deferred with the other value thresholds, and letter services receive no such advisory because the letter rule depends on goods value only and the EN and SV pages conflict on CN22 versus CN23 above SEK 2 000 (FN:98, FN:105-110, W and I).
PostNord requires the CN23 for International Parcel at every value, including non-commercial content such as gifts, samples, documents, and returned goods (FN:101, FN:111, W), and as of karrio-postnord 320f3ad the connector books the CN23 declaration data for it at every value when the booking carries customs commodities (S, `README.md` L163, `units.py` L499-L507).
Recorded gap, not addressed: for non-commercial International Parcel no advisory states that the printed CN23 must travel with the parcel, although PostNord's composition of the CN23 onto the label is verified only in a test-mode booking and not in production or for ZPL labels, and the separate CN23 is returned only with `postnord_standalone_customs_documents` set (S, karrio-postnord `README.md` L208, L212, and L219 at 320f3ad); the plugin returns no advisory for destinations other than Norway, and for Norway returns only `advisor_nordic_conventions_postnord_se_no_digital_invoice`, whose message does not mention the CN23.
Sources: FN:101-103 and FN:105-112 (W, verbatim web page and terms rules), FN:165-167 (S and W, code 91 is the contract product).

#### Scenario: Commercial Postpaket Utrikes to the United States

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to the United States is created with customs data whose `commercial_invoice` is true
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` at level `warning` stating the CN23, a commercial invoice in three copies, and that the connector sends CN23 declaration data and no invoice, returns the CN23 separately only with `postnord_standalone_customs_documents` set, that PostNord composed the CN23 onto the label in a test-mode booking and the connector checks PDF labels for it, and that production composition and ZPL labels are unverified, and its details list the terms with two copies, the web pages with triplicate, and the connector at karrio-postnord 320f3ad

#### Scenario: Sale-like content triggers the advisory

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to Switzerland is created with customs data whose `content_type` is `merchandise` and whose `commercial_invoice` is false
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice`

#### Scenario: Commercial Postpaket Utrikes to Norway sends the invoice digitally

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to Norway is created with customs data whose `commercial_invoice` is true
- **THEN** the plugin returns code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` stating the CN23 and the invoice sent digitally through the Booking API, Skicka Direkt Business, foravisering.export@postnord.com, or MyCustoms, without paper invoice copies, and its details cite the terms, the web pages, and the Norway rule

#### Scenario: Gift Postpaket Utrikes is not advised

- **WHEN** a PostNord `postnord_postpaket_utrikes` shipment from Sweden to Switzerland is created with customs data whose `content_type` is `gift` and whose `commercial_invoice` is false
- **THEN** the plugin does not return code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice`, although PostNord requires the CN23 for this shipment at every value (FN:101, FN:111, W); the connector sends the CN23 data, and the printed CN23 is a recorded gap the plugin does not advise

#### Scenario: Letters are not advised

- **WHEN** a commercial PostNord `postnord_export_letter` shipment from Sweden to Switzerland is created
- **THEN** the plugin does not return code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice`

#### Scenario: Finnish Postpaket Utrikes is not advised

- **WHEN** a commercial PostNord `postnord_postpaket_utrikes` shipment from Finland to Switzerland is created
- **THEN** the plugin does not return code `advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice`

### Requirement: DHL Freight Sweden needs a customs handling mode

For a DHL Freight Sweden shipment from Sweden to a destination outside the EU VAT area on which none of the connector's customs service options (standard handling, full-service handling, customer's own declaration, joint declaration) is set, the plugin SHALL return code `advisor_nordic_conventions_dhl_freight_sweden_customs_mode_missing` at level `warning`, stating that DHL requires customs handling (standard or full service), an own declaration, or a joint declaration to Norway or Switzerland to be selected for such destinations and naming the connector options that select them.
The joint declaration's destinations SHALL be the connector's `JOINT_DECLARATION_COUNTRIES`, Norway and Switzerland, outside which the connector refuses the joint declaration across the EU VAT area border (karrio-dhl-freight-sweden commit <https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/f86c8ac11fd9b017d4eb2a77bbf06fa88a1fa3fb>), copied into the plugin and checked against the connector by a test that runs when the connector is importable; the manual names Norway only (W, MAN v5.26 §6.8 p.98; S, connector README at <https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/blob/7a2214d26c0a8afef6e0bc3a4c4991c9e367988f/README.md>, citing product matches to NO and CH).
The connector selects no customs service implicitly because each carries a fee (S, connector README "Customs services" at 7a2214d); DHL's product manual requires the selection for Switzerland, Great Britain, Norway, Åland, and other non-EU destinations (FN:196, W, MAN v5.26 §7.6.1 p.163 and §6.7 p.96), and no fee-free mode exists for non-EU destinations (FN:208, W and I), which the details SHALL state.
For a recipient in Åland, as "DHL Freight Sweden customs handling is not selected to Åland" defines it, the plugin SHALL NOT return this code, because the connector accepts an Åland booking without a customs service, and DHL booked 109 to FI 22100 with customs data and no customs service (S, connector `docs/concepts/destinations.md` "Åland" at 7a2214d).

#### Scenario: No customs option to Norway

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created without any customs service option
- **THEN** the plugin returns code `advisor_nordic_conventions_dhl_freight_sweden_customs_mode_missing` at level `warning`, naming the joint declaration to Norway or Switzerland and its option `dhl_freight_sweden_customs_joint_declaration`

#### Scenario: Selected customs option silences the advisory

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with the full-service customs handling option set
- **THEN** the plugin does not return code `advisor_nordic_conventions_dhl_freight_sweden_customs_mode_missing`

#### Scenario: No customs option to Åland

- **WHEN** a DHL Freight Sweden shipment from Sweden to `FI` with postal code 22100, or to `AX` with postal code AX-22100, is created with customs data and without any customs service option
- **THEN** the plugin returns no customs-mode or Åland customs service code

### Requirement: DHL Freight Sweden VOEC ID is marked on the package

For a DHL Freight Sweden shipment from Sweden to Norway whose customs data carries `options.voec_number`, which the connector sends as DHL's VOEC supply VAT service (S, connector README "Customs services" at 7a2214d), the plugin SHALL return code `advisor_nordic_conventions_dhl_freight_sweden_voec_marking` at level `warning`, stating that the VOEC ID must be printed on the package or the label.
Sources: FN:217 (W, MAN v5.26 §6.5 p.92, §6.6 p.94, and §9.4.2 p.168), FN:206 (W, VOEC with Parcel Connect to Norway, sent in the API as `additionalServices.voecSupplyVAT.vatId` per MAN v5.26 §6.5 p.92 and §6.6 p.94).

#### Scenario: VOEC number to Norway

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data carrying a VOEC number
- **THEN** the plugin returns code `advisor_nordic_conventions_dhl_freight_sweden_voec_marking` at level `warning`

#### Scenario: No VOEC number

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data carrying no VOEC number
- **THEN** the plugin does not return code `advisor_nordic_conventions_dhl_freight_sweden_voec_marking`

### Requirement: The invoice type matches the content type

For an in-scope shipment whose booking carries an invoice type, meaning a PostNord parcel product or any DHL Freight Sweden service booked with customs data, the plugin SHALL return code `advisor_nordic_conventions_invoice_type_content_mismatch` at level `warning` when `customs.commercial_invoice` is false or omitted while the content is sale-like, and at level `info` when `customs.commercial_invoice` is true while `customs.content_type` is gift or sample.
For a PostNord parcel product the warning message SHALL state that the connector declares a proforma invoice from the flag (S, karrio-postnord `README.md` L187 and `shipment/create.py` L706-L710 at b03ddd0); for DHL Freight Sweden it SHALL state that the connector refuses the booking with `CommercialInvoiceRequiredError`, which it does across the EU VAT area border for sale-like content without `customs.commercial_invoice` true since karrio-dhl-freight-sweden commit <https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/ec180e61ca7ae4e763f58d9919ad9be0ae2ab56f> (S, connector README "Commercial or proforma invoice" at 7a2214d; `shipment/create.py` L513-L516 and L1062-L1090 at c878941); both warning messages SHALL state that a proforma invoice is for gifts and samples for which the recipient makes no payment, and that goods sold need `commercial_invoice` set to true; the info message SHALL state that a commercial invoice is declared for content described as a gift or sample, for which a proforma invoice is the usual document.
The levels differ because the sources restrict the proforma invoice to goods not sold but do not forbid a commercial invoice for gifts or samples.
Recorded gap, not addressed: the Postpaket Utrikes terms §2 permit a proforma invoice only for gifts or samples (FN:111, FN:113, W), but this advisory does not apply to International Parcel, whose booking carries no invoice type.
Recorded gap, not addressed: for International Parcel the connector sends CN23 declaration data and for letter services CN22 declaration data, and builds `customs.commercial_invoice`, `customs.invoice`, and `customs.invoice_date` only into the customs invoice of parcel products (S, karrio-postnord `units.py` L431-L439 and `shipment/create.py` L518-L571 and L890-L903 at b03ddd0), so it drops those fields for these services without a warning.
`advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` tells the consumer to supply the invoice for commercial International Parcel, and no advisory states the drop.
Sources: karrio-postnord `README.md` L187 at b03ddd0 (S, "`customs.commercial_invoice` | `type`: `COMMERCIAL` when true, `PROFORMA` when false or omitted"), karrio-dhl-freight-sweden `README.md` L348-L349 at 7a2214d (S, "True sends a `CommercialInvoice` document, and false or unset sends a `ProformaInvoice`." and the `CommercialInvoiceRequiredError` refusal), karrio-dhl-freight-sweden commit ec180e6 (S, the refusal's start), FN:56 (W, Bring tulldokument and DHL CIE p.5, a proforma invoice is used for goods not sold), FN:111 and FN:113 (W, Postpaket Utrikes terms §2, "Proformafaktura … får endast användas vid gåva eller varuprov").

#### Scenario: Merchandise declared as proforma

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data whose `content_type` is `merchandise` and whose `commercial_invoice` is omitted
- **THEN** the plugin returns code `advisor_nordic_conventions_invoice_type_content_mismatch` at level `warning` stating that the connector refuses the booking with `CommercialInvoiceRequiredError`, and not that it declares a proforma invoice

#### Scenario: Omitted content type declared as proforma

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying no `content_type` and `commercial_invoice` false
- **THEN** the plugin returns code `advisor_nordic_conventions_invoice_type_content_mismatch` at level `warning` stating that the connector declares a proforma invoice

#### Scenario: Gift declared as proforma is consistent

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data whose `content_type` is `gift` and whose `commercial_invoice` is false
- **THEN** the plugin does not return code `advisor_nordic_conventions_invoice_type_content_mismatch`

#### Scenario: Return merchandise declared as proforma is consistent

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data whose `content_type` is `return_merchandise` and whose `commercial_invoice` is false
- **THEN** the plugin does not return code `advisor_nordic_conventions_invoice_type_content_mismatch`

#### Scenario: Sample declared as commercial is informational

- **WHEN** a DHL Freight Sweden shipment from Sweden to Switzerland is created with customs data whose `content_type` is `sample` and whose `commercial_invoice` is true
- **THEN** the plugin returns code `advisor_nordic_conventions_invoice_type_content_mismatch` at level `info`

#### Scenario: Letters carry no invoice type

- **WHEN** a PostNord `postnord_export_letter` shipment from Sweden to Norway is created with customs data whose `content_type` is `merchandise` and whose `commercial_invoice` is false
- **THEN** the plugin does not return code `advisor_nordic_conventions_invoice_type_content_mismatch`, because the connector sends a CN22 without an invoice type for letters

### Requirement: Contradicted attestations are reported

When an attested procedure is contradicted by the conventions that govern the lane, the plugin SHALL return code `advisor_nordic_conventions_attestation_conflict` at level `warning`, once per contradicted attestation, naming the attested procedure and the contradicting convention, with the convention's sources in `details`.
In this change the only contradiction is `advisor_nordic_conventions_commercial_invoice_paper_copy` on a PostNord lane from Sweden to Norway, whose sources require the commercial invoice digitally and not on paper with the parcel (FN:118, FN:142, W; S, karrio-postnord `README.md` L157 and L160 at b03ddd0).

#### Scenario: Paper invoice attested on the Sweden-to-Norway lane

- **WHEN** `advisor_nordic_conventions_commercial_invoice_paper_copy` is attested on a PostNord shipment from Sweden to Norway
- **THEN** the conflict warning is returned, naming the digital-only convention and its sources

#### Scenario: No contradiction, no conflict message

- **WHEN** every attestation holds on the lane
- **THEN** the attestations cover their procedures and no conflict advisory is returned


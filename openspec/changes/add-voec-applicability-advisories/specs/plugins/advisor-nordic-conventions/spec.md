# Spec Delta

## ADDED Requirements

### Requirement: VOEC shipments to Norway carry no goods excluded from VOEC

For a shipment within the plugin's scope to Norway whose customs data carries `options.voec_number`, the plugin SHALL return code `advisor_nordic_conventions_voec_excluded_goods` at level `warning` when at least one commodity's HS code falls in an excluded class.
The HS code SHALL be read as its digits only, and a commodity without an HS code SHALL NOT be classified.
The excluded classes SHALL be: foodstuffs, chapters 02-04, 07-13, and 15-21 except headings 1209, 1518, 1520, 1521, and 1522, together with headings 2201, 2202, 2209, and 2936; alcohol, headings 2203-2208; tobacco, chapter 24; pharmaceuticals, chapter 30; and arms and ammunition, chapter 93.
Chapters 01, 05, 06, 14, and 23 SHALL NOT be classified.
The message SHALL name each triggering commodity by its `description`, else its `title`, else its `sku`, else its zero-based line index, together with its class, and SHALL state that VOEC does not cover foodstuffs, goods requiring an import permit, or excise goods, so the consignment must be split or the whole shipment declared at the border with VAT collected on import.
`details` SHALL list the zero-based indexes of the triggering commodities under `lines` and their classes under `classes`, in the same order.
`details` SHALL cite Skatteetaten's VOEC guidelines §3 and §4.1 (W, `SKE_VOEC_EXCLUDED_GOODS`, `SKE_VOEC_MIXED_CONSIGNMENT`), Tolletaten's "Om VOEC-ordningen" page (W, `TOLL_VOEC_EXCLUDED_GOODS`), merverdiavgiftsloven § 3-1 (2) and § 5-2 (W, `MVAL_LOW_VALUE_EXCLUSIONS`, `MVAL_FOODSTUFFS`), merverdiavgiftsforskriften § 5-2-1 (W, `MVAF_FOODSTUFFS`), and the HS class mapping over Tolletaten's tariff structure (I, `HS_VOEC_EXCLUDED_CLASSES`).

#### Scenario: Food supplement in a VOEC shipment

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number whose second commodity, described "Protein powder", has HS code `2106.90`
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_excluded_goods` at level `warning` with `lines` [1] and `classes` ["foodstuffs"], naming "Protein powder"

#### Scenario: Wine in a VOEC shipment

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity with HS code `220421`
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_excluded_goods` with `classes` ["alcohol"]

#### Scenario: Item named by its SKU

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity with HS code `3004.90`, no description or title, and SKU `VIT-100`
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_excluded_goods` naming `VIT-100` with class "pharmaceuticals"

#### Scenario: Animal feed is not a foodstuff

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a single commodity with HS code `2309.10`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_excluded_goods`

#### Scenario: Beeswax is not a foodstuff

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a single commodity with HS code `1521.90`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_excluded_goods`

#### Scenario: Commodity without an HS code

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a single commodity described "Chocolate" with no HS code
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_excluded_goods`

#### Scenario: No VOEC number

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying no VOEC number and a commodity with HS code `2106.90`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_excluded_goods`

#### Scenario: VOEC number to another destination

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Switzerland is created with customs data carrying a VOEC number and a commodity with HS code `2106.90`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_excluded_goods`

### Requirement: VOEC shipments to Norway carry no item at or above NOK 3,000

For a shipment within the plugin's scope to Norway whose customs data carries `options.voec_number`, the plugin SHALL return code `advisor_nordic_conventions_voec_item_over_threshold` at level `warning` when at least one commodity's unit value is at or above the VOEC limit.
A commodity's unit value SHALL be its `value_amount` in its `value_currency`, independent of its `quantity`, because karrio's `value_amount` is the value of one unit.
A unit value in NOK SHALL count as at or above the limit when it is at least 3,000.
A unit value in SEK, EUR, DKK, or USD SHALL be converted to NOK at the plugin's dated Norges Bank rate and SHALL count as at or above the limit only when the converted value is at least 3,150, which is NOK 3,000 with a 5 % margin.
A commodity with no value, a value of 0, no currency, or a currency outside that table SHALL NOT be evaluated.
The message SHALL name each triggering commodity as the excluded-goods advisory names it, and SHALL state that VOEC applies per item below NOK 3,000 excluding shipping and insurance, and that an item at or above it goes through ordinary import declaration, so the consignment must be split or the whole shipment declared at the border.
`details` SHALL list the zero-based indexes of the triggering commodities under `lines`, state the rate date under `rate_date`, and cite Skatteetaten's VOEC guidelines §4 and §4.1 (W, `SKE_VOEC_PER_ITEM_THRESHOLD`, `SKE_VOEC_MIXED_CONSIGNMENT`), Tolletaten's "Om VOEC-ordningen" page (W, `TOLL_VOEC_PER_ITEM_THRESHOLD`), merverdiavgiftsforskriften § 1-3-8 (W, `MVAF_LOW_VALUE_GOODS`), and the Norges Bank exchange rates (W, `NORGES_BANK_RATES`).

#### Scenario: Item at NOK 3,000

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity of `value_amount` 3000 in NOK
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_item_over_threshold` at level `warning` with `lines` [0]

#### Scenario: Item just below NOK 3,000

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity of `value_amount` 2999 in NOK
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_item_over_threshold`

#### Scenario: Item clearly over in SEK

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity of `value_amount` 5000 in SEK
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_item_over_threshold`

#### Scenario: Converted item inside the margin

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity in EUR whose `value_amount` converts at the table rate to a value from NOK 3,000 up to but not including NOK 3,150
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_item_over_threshold`

#### Scenario: Several units below the limit

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity of `value_amount` 2000 in NOK with `quantity` 3
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_item_over_threshold`

#### Scenario: Currency outside the table

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a commodity of `value_amount` 5000 in GBP
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_item_over_threshold`

#### Scenario: No VOEC number

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying no VOEC number and a commodity of `value_amount` 5000 in NOK
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_item_over_threshold`

### Requirement: VOEC shipments to Norway go to consumers

For a shipment within the plugin's scope to Norway whose customs data carries `options.voec_number` and whose recipient carries a non-blank `federal_tax_id` or `state_tax_id`, the plugin SHALL return code `advisor_nordic_conventions_voec_business_recipient` at level `warning`.
The message SHALL state that VOEC covers sales to consumers only, and that a business buyer self-assesses the VAT, so VOEC VAT must not be charged.
`details` SHALL cite Skatteetaten's B2B guide (W, `SKE_VOEC_B2B`), Skatteetaten's VOEC guidelines §10.1 (W, `SKE_VOEC_B2C_ONLY`), and merverdiavgiftsloven § 3-1 (2) (W, `MVAL_LOW_VALUE_EXCLUSIONS`).

#### Scenario: Recipient with an organisation number

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a recipient whose `federal_tax_id` is `912345678`
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_business_recipient` at level `warning`

#### Scenario: Recipient with a state tax id

- **WHEN** a DHL Freight Sweden shipment from Sweden to Norway is created with customs data carrying a VOEC number and a recipient whose `state_tax_id` is set
- **THEN** the plugin returns code `advisor_nordic_conventions_voec_business_recipient`

#### Scenario: Consumer recipient

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying a VOEC number and a recipient with neither `federal_tax_id` nor `state_tax_id`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_business_recipient`

#### Scenario: Business recipient without a VOEC number

- **WHEN** a PostNord `postnord_parcel` shipment from Sweden to Norway is created with customs data carrying no VOEC number and a recipient whose `federal_tax_id` is `912345678`
- **THEN** the plugin does not return code `advisor_nordic_conventions_voec_business_recipient`

## MODIFIED Requirements

### Requirement: Advisory answering procedures

The plugin SHALL hold, for every advisory classification, the set of procedures whose performance answers it; the set is empty when no out-of-booking procedure answers it, and the plugin SHALL keep the mapping complete over all classifications.
`advisor_nordic_conventions_dhl_freight_sweden_customs_mode_missing`, `advisor_nordic_conventions_dhl_freight_sweden_aland_customs_service_rejected`, `advisor_nordic_conventions_dhl_freight_sweden_joint_declaration_destination`, and `advisor_nordic_conventions_invoice_type_content_mismatch` SHALL map to the empty set, because their remedy lies inside the booking request, in the connector's customs service options and the `customs.commercial_invoice` flag.
The answering sets SHALL be lane-aware as follows.
`advisor_nordic_conventions_postnord_se_no_digital_invoice` is answered by `commercial_invoice_electronic`.
`advisor_nordic_conventions_postnord_se_postpaket_commercial_invoice` is answered, for Norway, by `customs_declaration_paper_copy` and `commercial_invoice_electronic`, and for other destinations by `customs_declaration_paper_copy` and `commercial_invoice_paper_copy`, resting on the terms' CN23 in two copies and invoice copies with the parcel (FN:103, FN:111, W).
`advisor_nordic_conventions_postnord_se_export_paper_invoice` is answered by `commercial_invoice_paper_copy`.
`advisor_nordic_conventions_postnord_fi_export_invoice` is answered, for Norway, by `commercial_invoice_electronic`, and for other destinations by `commercial_invoice_paper_copy`.
`advisor_nordic_conventions_postnord_dk_export_documents` is answered, for Norway, Switzerland, and Liechtenstein, and Great Britain, by `commercial_invoice_paper_copy`, and for any other destination by `customs_declaration_paper_copy` and `commercial_invoice_paper_copy`, resting on the 1 CN23 and 2 invoices default (FN:144, W).
`advisor_nordic_conventions_dhl_freight_sweden_invoice_copy` is answered by `commercial_invoice_electronic`.
`advisor_nordic_conventions_dhl_freight_sweden_attached_documents` is answered by `customs_documents_attached_outside`.
`advisor_nordic_conventions_dhl_freight_sweden_voec_marking` is answered by `voec_marking_printed`.
`advisor_nordic_conventions_ch_discount_on_invoice`, `advisor_nordic_conventions_zero_value_line`, `advisor_nordic_conventions_dhl_freight_sweden_parcel_connect_not_served`, `advisor_nordic_conventions_dhl_freight_sweden_parcel_connect_gb_agreement`, and `advisor_nordic_conventions_dhl_freight_sweden_territory_postal_code_mismatch` SHALL map to the empty set, because their remedy lies in the invoice content, the declared values, the booked product, or the address.
`advisor_nordic_conventions_voec_excluded_goods`, `advisor_nordic_conventions_voec_item_over_threshold`, and `advisor_nordic_conventions_voec_business_recipient` SHALL map to the empty set, because their remedy lies in the consignment's content, its split, or the VAT charged to the buyer.

#### Scenario: Mapping is complete

- **WHEN** the plugin adds an advisory classification
- **THEN** its answering set is defined, and an omitted entry is a test failure

#### Scenario: Finland to Norway answers electronically

- **WHEN** `advisor_nordic_conventions_postnord_fi_export_invoice` applies to a Norway destination
- **THEN** its answering set is `commercial_invoice_electronic` alone

#### Scenario: Denmark default destination needs both paper procedures

- **WHEN** `advisor_nordic_conventions_postnord_dk_export_documents` applies to a destination other than Norway, Switzerland, Liechtenstein, and Great Britain
- **THEN** its answering set is `customs_declaration_paper_copy` and `commercial_invoice_paper_copy`

#### Scenario: VOEC applicability advisories are unanswerable

- **WHEN** `advisor_nordic_conventions_voec_excluded_goods`, `advisor_nordic_conventions_voec_item_over_threshold`, or `advisor_nordic_conventions_voec_business_recipient` applies
- **THEN** its answering set is empty and no attestation omits it

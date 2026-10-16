# Proposal

## Why

A consumer that books a shipment to Norway with `customs.options.voec_number` set declares that Norwegian VAT was collected at the point of sale under the VOEC scheme.
The scheme covers only sales of low value goods to consumers, and the official sources exclude three cases that the plugin can see in the shipment request.
Skatteetaten's VOEC guidelines (modified 2025-03-28), Tolletaten's "Om VOEC-ordningen" page (updated 2025-11-27), and merverdiavgiftsloven § 3-1 (2) exclude foodstuffs, goods requiring an import permit, and excise goods.
The guidelines §4 and merverdiavgiftsforskriften § 1-3-8 apply the NOK 3,000 limit per item, excluding shipping and insurance.
Skatteetaten's B2B guide (2026-02-04) states that a business buyer is not charged VOEC VAT.
No advisory relays any of these today; the only VOEC advisory, `advisor_nordic_conventions_dhl_freight_sweden_voec_marking`, concerns the label.

## What Changes

- Adds `advisor_nordic_conventions_voec_excluded_goods` at level `warning`: a shipment to Norway with a VOEC number whose commodities include an item whose HS code falls in a class the plugin reads as excluded from VOEC (foodstuffs, alcohol, tobacco, pharmaceuticals, arms and ammunition).
- Adds `advisor_nordic_conventions_voec_item_over_threshold` at level `warning`: a shipment to Norway with a VOEC number whose commodities include an item whose unit value, converted to NOK at a dated Norges Bank rate, is clearly at or above NOK 3,000.
- Adds `advisor_nordic_conventions_voec_business_recipient` at level `warning`: a shipment to Norway with a VOEC number whose recipient carries a `federal_tax_id` or `state_tax_id`.
- Maps the three codes to the empty answering set, because their remedy lies in the consignment's content, its split, or the VAT charged to the buyer.
- Adds a dated exchange rate table for SEK, EUR, DKK, USD, and NOK, and an HS classifier over tariff chapters and headings, both cited.
- Narrows the documented non-goal "No goods-value thresholds" so VOEC's per-item NOK 3,000 is the stated exception.

Out of scope: description-keyword classification of goods without an HS code, excise goods beyond alcohol and tobacco (sugar, beverage packaging, lubricating oil, gases), restricted goods beyond the listed chapters, the VOEC split prohibition (a recorded non-goal), attestations answering the new advisories, and connector changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugins/advisor-nordic-conventions`: three advisory requirements are added, and the answering-procedures requirement maps the new codes to the empty set.

## Impact

`codes.py`, `sources.py`, a new `rates.py`, a new `rules/voec.py`, `procedures.py` (rule registration and answering map), tests, `docs/concepts/advisories.md`, `docs/concepts/scope.md`, `README.md`, and the main specification.
Advisory codes are public API: three are added and none is renamed.

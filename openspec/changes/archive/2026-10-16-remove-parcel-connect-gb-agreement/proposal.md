# Proposal

## Why

`advisor_nordic_conventions_dhl_freight_sweden_parcel_connect_gb_agreement` warns, at shipment creation, on every DHL Freight Sweden Parcel Connect (109) or Parcel Connect Plus (112) shipment from Sweden to Great Britain that these products serve Great Britain only by separate agreement with DHL (product manual v5.26 §5.3 p.18, §5.14 p.63).
The DHL Freight Sweden connector now covers the same lane at the same stage.
Its booking guard runs DHL's Product API product matches before every booking by default (connection setting `product_matches`, default `enforce`) and refuses 109 or 112 when DHL does not offer the product on the lane, with a message naming the separate agreement (karrio-dhl-freight-sweden 0a1556b).
When the guard is off or cannot verify the product, DHL's own 22005 and 22026 rejections of 109 or 112 to Great Britain carry a `separate_agreement_lane` warning naming the agreement (karrio-dhl-freight-sweden 7a6dd9e).
The advisory adds nothing to either path, and it warns on every booking of a shipper that holds the agreement, where the connector stays silent.

## What Changes

- Removes the advisory code `advisor_nordic_conventions_dhl_freight_sweden_parcel_connect_gb_agreement`, its rule, its answering-procedures entry, and the two sources only it cites (`DHL_MAN_PARCEL_CONNECT_COUNTRIES` and `DHL_CONNECTOR_SANDBOX_112_GB_REJECTED`, with the URL constant `DHL_CONNECTOR_REJECTION_112_GB_URL`).
- Removes its row, Codes list line, and footnote from `docs/concepts/advisories.md`, and its two cells from the README's Requirements at a glance matrix.
- Pins the Isle of Man territory reading through the invoice copy fee instead of the removed advisory.

The removal is breaking for any consumer that matches on the code; no alias or deprecation period is kept, because the plugin is in early development.
109 and 112 to Great Britain stay outside `advisor_nordic_conventions_dhl_freight_sweden_parcel_connect_not_served`, because the manual lists Great Britain among their valid countries.

Out of scope: any connector change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugins/advisor-nordic-conventions`: removes "DHL Freight Sweden Parcel Connect serves Great Britain only by separate agreement" and modifies "Advisory answering procedures", "DHL Freight Sweden products are not booked on lanes they do not serve", and "DHL Freight Sweden territory codes are read as their parent country".

## Impact

`codes.py`, `procedures.py`, `sources.py`, `rules/dhl_freight_sweden.py`, tests, `README.md`, `docs/concepts/advisories.md`, and the main specification.
One advisory code disappears; no other code, level, message, or attestation changes.

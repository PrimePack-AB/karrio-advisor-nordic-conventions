"""VOEC applicability advisories on shipments to Norway that carry a VOEC number."""

import typing

import karrio.plugins.advisor_nordic_conventions.exclusions as exclusions
import karrio.plugins.advisor_nordic_conventions.lanes as lanes

# Jan Mayen (8099) and Svalbard (9170-9179) in Posten's postal code register,
# outside the Norwegian VAT area; the whole Svalbard range is matched so a code
# Posten later assigns in it is covered.
OUTSIDE_VAT_AREA_POSTAL_CODES: typing.Tuple[typing.Tuple[int, int], ...] = (
    (8099, 8099),
    (9170, 9179),
)


def outside_vat_area(postal_code: typing.Optional[str]) -> bool:
    """Whether a Norwegian postal code lies in Jan Mayen or Svalbard; a missing or malformed code reads as the mainland."""
    key = exclusions.postal_code_key(lanes.NORWAY, postal_code)
    return key is not None and any(low <= key <= high for low, high in OUTSIDE_VAT_AREA_POSTAL_CODES)


def voec_lane(request: typing.Any, context: typing.Any) -> typing.Optional[lanes.Lane]:
    """The lane of an in-scope shipment to the Norwegian VAT area carrying a VOEC number, else None."""
    lane = lanes.lane_of(request, context)

    if lane is None or not lane.to_norway or not lane.voec_number:
        return None

    if outside_vat_area(getattr(getattr(request, "recipient", None), "postal_code", None)):
        return None

    return lane

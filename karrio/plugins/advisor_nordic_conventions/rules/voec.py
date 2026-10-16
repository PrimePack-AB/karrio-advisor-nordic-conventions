"""VOEC applicability advisories on shipments to Norway that carry a VOEC number."""

import enum
import re
import typing

import karrio.core.models as models

import karrio.plugins.advisor_nordic_conventions.exclusions as exclusions
import karrio.plugins.advisor_nordic_conventions.lanes as lanes
import karrio.plugins.advisor_nordic_conventions.rates as rates
import karrio.plugins.advisor_nordic_conventions.sources as sources
from karrio.plugins.advisor_nordic_conventions.codes import AdvisoryClassification
from karrio.plugins.advisor_nordic_conventions.rules import advisory

# Jan Mayen (8099) and Svalbard (9170-9179) in Posten's postal code register,
# outside the Norwegian VAT area; the whole Svalbard range is matched so a code
# Posten later assigns in it is covered.
OUTSIDE_VAT_AREA_POSTAL_CODES: typing.Tuple[typing.Tuple[int, int], ...] = (
    (8099, 8099),
    (9170, 9179),
)


class ExcludedClass(str, enum.Enum):
    """A class of goods the plugin reads as excluded from VOEC."""

    foodstuffs = "foodstuffs"
    alcohol = "alcohol"
    tobacco = "tobacco"
    pharmaceuticals = "pharmaceuticals"
    arms_and_ammunition = "arms and ammunition"
    restricted = "restricted"


def _chapters(classification: ExcludedClass, *chapters: int) -> typing.Dict[str, ExcludedClass]:
    return {f"{chapter:02d}": classification for chapter in chapters}


# An inference over Tolltariffen's chapter and heading texts
# (sources.HS_VOEC_EXCLUDED_CLASSES); no source maps HS codes to the exclusions.
CHAPTER_CLASSES: typing.Dict[str, ExcludedClass] = {
    **_chapters(ExcludedClass.foodstuffs, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21),
    **_chapters(ExcludedClass.tobacco, 24),
    **_chapters(ExcludedClass.pharmaceuticals, 30),
    **_chapters(ExcludedClass.arms_and_ammunition, 93),
    **_chapters(ExcludedClass.restricted, 1, 6),
}
HEADING_CLASSES: typing.Dict[str, typing.Optional[ExcludedClass]] = {
    "1209": ExcludedClass.restricted,
    "1518": None,
    "1520": None,
    "1521": None,
    "1522": None,
    "2201": ExcludedClass.foodstuffs,
    "2202": ExcludedClass.foodstuffs,
    "2209": ExcludedClass.foodstuffs,
    "2936": ExcludedClass.foodstuffs,
    **{str(heading): ExcludedClass.alcohol for heading in range(2203, 2209)},
}


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


def hs_class(hs_code: typing.Optional[str]) -> typing.Optional[ExcludedClass]:
    """The excluded class of an HS code read as its digits, a listed heading before its chapter, else None."""
    digits = re.sub(r"\D", "", str(hs_code or ""))

    if len(digits) >= 4 and digits[:4] in HEADING_CLASSES:
        return HEADING_CLASSES[digits[:4]]

    return CHAPTER_CLASSES.get(digits[:2]) if len(digits) >= 2 else None


def item_name(index: int, commodity: typing.Any) -> str:
    """A commodity's description, else its title, else its SKU, else its zero-based line."""
    return next(
        (
            text
            for text in (
                str(getattr(commodity, field, None) or "").strip()
                for field in ("description", "title", "sku")
            )
            if text
        ),
        f"line {index}",
    )


def _commodities(request: typing.Any) -> typing.List[typing.Any]:
    customs = getattr(request, "customs", None)
    return list(getattr(customs, "commodities", None) or [])


VAT_AREA_SOURCES = (
    sources.MVAL_VAT_AREA,
    sources.SKE_VOEC_VAT_AREA,
    sources.BRING_SVALBARD_JAN_MAYEN_POSTAL_CODES,
)


def voec_excluded_goods(request, context) -> typing.List[models.Message]:
    lane = voec_lane(request, context)

    if lane is None:
        return []

    excluded = [
        (index, commodity, classification)
        for index, commodity in enumerate(_commodities(request))
        for classification in [hs_class(getattr(commodity, "hs_code", None))]
        if classification is not None
    ]

    if not excluded:
        return []

    items = ", ".join(
        f"{item_name(index, commodity)} ({classification.value})"
        for index, commodity, classification in excluded
    )

    return [
        advisory(
            AdvisoryClassification.voec_excluded_goods,
            "warning",
            " ".join(
                [
                    f"This VOEC shipment to Norway carries {items}.",
                    "VOEC does not cover foodstuffs, goods requiring an import permit, or excise goods,",
                    "so the consignment must be split or the whole shipment declared at the border",
                    "with VAT collected on import.",
                ]
            ),
            lane,
            [
                sources.SKE_VOEC_EXCLUDED_GOODS,
                sources.SKE_VOEC_MIXED_CONSIGNMENT,
                sources.TOLL_VOEC_EXCLUDED_GOODS,
                sources.MVAL_LOW_VALUE_EXCLUSIONS,
                sources.MVAL_FOODSTUFFS,
                sources.MVAF_FOODSTUFFS,
                sources.SKE_VOEC_RESTRICTED_EXAMPLES,
                sources.HS_VOEC_EXCLUDED_CLASSES,
                *VAT_AREA_SOURCES,
            ],
            lines=[index for index, _, _ in excluded],
            classes=[classification.value for _, _, classification in excluded],
        )
    ]


def at_or_above_limit(commodity: typing.Any) -> bool:
    """Whether a commodity's unit value reaches NOK 3,000, or for a converted currency NOK 3,000 with the margin."""
    amount = getattr(commodity, "value_amount", None)
    currency = str(getattr(commodity, "value_currency", None) or "").upper()
    nok = rates.to_nok(amount, currency) if amount else None

    if nok is None:
        return False

    limit = rates.VOEC_LIMIT_NOK if currency == "NOK" else rates.VOEC_LIMIT_NOK * rates.MARGIN
    return nok >= limit


def voec_item_over_threshold(request, context) -> typing.List[models.Message]:
    lane = voec_lane(request, context)

    if lane is None:
        return []

    over = [
        (index, commodity)
        for index, commodity in enumerate(_commodities(request))
        if at_or_above_limit(commodity)
    ]

    if not over:
        return []

    items = ", ".join(item_name(index, commodity) for index, commodity in over)

    return [
        advisory(
            AdvisoryClassification.voec_item_over_threshold,
            "warning",
            " ".join(
                [
                    f"This VOEC shipment to Norway carries {items}, each with a unit value at or above NOK 3,000.",
                    "VOEC applies per item below NOK 3,000, excluding shipping and insurance,",
                    "and an item at or above it goes through ordinary import declaration,",
                    "so the consignment must be split or the whole shipment declared at the border.",
                ]
            ),
            lane,
            [
                sources.SKE_VOEC_PER_ITEM_THRESHOLD,
                sources.SKE_VOEC_MIXED_CONSIGNMENT,
                sources.TOLL_VOEC_PER_ITEM_THRESHOLD,
                sources.MVAF_LOW_VALUE_GOODS,
                sources.NORGES_BANK_RATES,
                *VAT_AREA_SOURCES,
            ],
            lines=[index for index, _ in over],
            rate_date=rates.RATE_DATE,
        )
    ]


def _has_tax_id(party: typing.Any) -> bool:
    return any(
        str(getattr(party, field, None) or "").strip() for field in ("federal_tax_id", "state_tax_id")
    )


def voec_business_recipient(request, context) -> typing.List[models.Message]:
    lane = voec_lane(request, context)

    if lane is None or not _has_tax_id(getattr(request, "recipient", None)):
        return []

    return [
        advisory(
            AdvisoryClassification.voec_business_recipient,
            "warning",
            " ".join(
                [
                    "This VOEC shipment to Norway goes to a recipient with a tax id.",
                    "VOEC covers sales to consumers only, and a business buyer self-assesses the VAT,",
                    "so VOEC VAT must not be charged.",
                ]
            ),
            lane,
            [
                sources.SKE_VOEC_B2B,
                sources.SKE_VOEC_B2C_ONLY,
                sources.MVAL_LOW_VALUE_EXCLUSIONS,
                *VAT_AREA_SOURCES,
            ],
        )
    ]

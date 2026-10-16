import decimal
import unittest
from unittest import mock

import karrio.core.models as models
import karrio.lib as lib

import karrio.plugins.advisor_nordic_conventions.rates as rates
import karrio.plugins.advisor_nordic_conventions.rules.voec as voec
import karrio.plugins.advisor_nordic_conventions.sources as sources
from . import fixture

VOEC_NUMBER = "VOEC2024001"
DHL_PARCEL_CONNECT = "dhl_freight_sweden_parcel_connect_b2c"
EXCLUDED_GOODS = "advisor_nordic_conventions_voec_excluded_goods"

T_SHIRT = fixture.COMMODITIES[0]


def _commodity(**fields) -> dict:
    return dict(
        dict(quantity=1, weight=0.5, weight_unit="KG", value_amount=200.0, value_currency="SEK", origin_country="SE"),
        **fields,
    )


PROTEIN_POWDER = _commodity(description="Protein powder", hs_code="2106.90")
WINE = _commodity(description="Wine", hs_code="220421")
OLIVE_TREE = _commodity(description="Olive tree", hs_code="0602.90")
VITAMINS_BY_SKU = _commodity(sku="VIT-100", hs_code="3004.90")
DOG_FOOD = _commodity(description="Dog food", hs_code="2309.10")
BEESWAX = _commodity(description="Beeswax", hs_code="1521.90")
UNCODED_CHOCOLATE = _commodity(description="Chocolate")
ITEM_OVER_THRESHOLD = "advisor_nordic_conventions_voec_item_over_threshold"
BUSINESS_RECIPIENT = "advisor_nordic_conventions_voec_business_recipient"


def _valued(amount, currency, quantity=1, description="Road bike") -> dict:
    return _commodity(description=description, value_amount=amount, value_currency=currency, quantity=quantity)

SVALBARD_SOURCES = [
    sources.MVAL_VAT_AREA.to_dict(),
    sources.SKE_VOEC_VAT_AREA.to_dict(),
    sources.BRING_SVALBARD_JAN_MAYEN_POSTAL_CODES.to_dict(),
]
EXCLUDED_GOODS_SOURCES = [
    sources.SKE_VOEC_EXCLUDED_GOODS.to_dict(),
    sources.SKE_VOEC_MIXED_CONSIGNMENT.to_dict(),
    sources.TOLL_VOEC_EXCLUDED_GOODS.to_dict(),
    sources.MVAL_LOW_VALUE_EXCLUSIONS.to_dict(),
    sources.MVAL_FOODSTUFFS.to_dict(),
    sources.MVAF_FOODSTUFFS.to_dict(),
    sources.SKE_VOEC_RESTRICTED_EXAMPLES.to_dict(),
    sources.HS_VOEC_EXCLUDED_CLASSES.to_dict(),
    *SVALBARD_SOURCES,
]


def _advise(advisor, *commodities, recipient="NO", carrier="postnord", service="postnord_parcel", voec_number=VOEC_NUMBER):
    options = dict(voec_number=voec_number) if voec_number else None
    customs = lib.to_dict(
        dict(commodities=list(commodities), content_type="merchandise", commercial_invoice=True, options=options)
    )
    request = fixture.shipment("SE", recipient, service, customs=customs)
    return fixture.messages(advisor, request, fixture.context(carrier))


def _codes(messages) -> list:
    return [message["code"] for message in messages]


def _voec_shipment(recipient: str, service: str = "postnord_parcel", voec_number=VOEC_NUMBER):
    options = dict(voec_number=voec_number) if voec_number else {}
    return fixture.shipment("SE", recipient, service, customs=fixture.customs("merchandise", True, **options))


class TestNordicConventionsVoecVatArea(unittest.TestCase):
    def test_svalbard_and_jan_mayen_postal_codes_are_outside(self):
        self.assertListEqual(
            [code for code in ("8099", "9170", "9171", "9179") if not voec.outside_vat_area(code)],
            [],
        )

    def test_other_missing_and_malformed_postal_codes_are_inside(self):
        self.assertListEqual(
            [code for code in ("8098", "9180", "0150", None, "", "91 7X") if voec.outside_vat_area(code)],
            [],
        )

    def test_voec_lane_to_mainland_norway(self):
        lane = voec.voec_lane(_voec_shipment("NO"), fixture.context("postnord"))

        self.assertEqual(lane.recipient_country, "NO")
        self.assertEqual(lane.voec_number, VOEC_NUMBER)

    def test_voec_lane_without_a_postal_code_reads_as_mainland(self):
        self.assertIsNotNone(voec.voec_lane(_voec_shipment("NO_NO_POSTAL_CODE"), fixture.context("postnord")))

    def test_no_voec_lane_to_svalbard_by_postal_code(self):
        self.assertIsNone(voec.voec_lane(_voec_shipment("NO_SVALBARD"), fixture.context("postnord")))

    def test_no_voec_lane_to_jan_mayen_by_postal_code(self):
        self.assertIsNone(voec.voec_lane(_voec_shipment("NO_JAN_MAYEN"), fixture.context("postnord")))

    def test_no_voec_lane_to_the_svalbard_and_jan_mayen_country_code(self):
        self.assertIsNone(voec.voec_lane(_voec_shipment("SJ"), fixture.context("postnord")))

    def test_no_voec_lane_without_a_voec_number(self):
        self.assertIsNone(voec.voec_lane(_voec_shipment("NO", voec_number=None), fixture.context("postnord")))



class TestNordicConventionsVoecHsClassifier(unittest.TestCase):
    def test_classes_of_listed_chapters_and_headings(self):
        expected = {
            "0201": "foodstuffs",
            "0302": "foodstuffs",
            "0406": "foodstuffs",
            "0709": "foodstuffs",
            "0801": "foodstuffs",
            "0901": "foodstuffs",
            "1006": "foodstuffs",
            "1101": "foodstuffs",
            "1211": "foodstuffs",
            "1302": "foodstuffs",
            "1509": "foodstuffs",
            "1601": "foodstuffs",
            "1704": "foodstuffs",
            "1806": "foodstuffs",
            "1905": "foodstuffs",
            "2009": "foodstuffs",
            "2106": "foodstuffs",
            "2201": "foodstuffs",
            "2202": "foodstuffs",
            "2209": "foodstuffs",
            "2936": "foodstuffs",
            "2203": "alcohol",
            "2204": "alcohol",
            "2205": "alcohol",
            "2206": "alcohol",
            "2207": "alcohol",
            "2208": "alcohol",
            "2402": "tobacco",
            "3004": "pharmaceuticals",
            "9303": "arms and ammunition",
            "0101": "restricted",
            "0602": "restricted",
            "1209": "restricted",
        }

        self.assertDictEqual({code: voec.hs_class(code) for code in expected}, expected)

    def test_carved_out_headings_and_unlisted_chapters_are_unclassified(self):
        self.assertListEqual(
            [
                code
                for code in ("1518", "1520", "1521", "1522", "0511", "1404", "2309", "2210", "2937", "6109")
                if voec.hs_class(code) is not None
            ],
            [],
        )

    def test_hs_code_is_read_as_its_digits(self):
        self.assertEqual(voec.hs_class("2106.90"), "foodstuffs")
        self.assertEqual(voec.hs_class("2204 21"), "alcohol")
        self.assertEqual(voec.hs_class("22"), None)
        self.assertEqual(voec.hs_class("24"), "tobacco")

    def test_missing_or_short_hs_code_is_unclassified(self):
        self.assertListEqual([code for code in (None, "", "2", "..") if voec.hs_class(code) is not None], [])

    def test_item_name_falls_back_from_description_to_title_sku_and_line(self):
        commodities = lib.to_object(
            models.Customs,
            dict(
                commodities=[
                    _commodity(description="Protein powder", title="Whey", sku="W-1"),
                    _commodity(title="Whey", sku="W-1"),
                    _commodity(sku="W-1"),
                    _commodity(),
                ]
            ),
        ).commodities

        self.assertListEqual(
            [voec.item_name(index, commodity) for index, commodity in enumerate(commodities)],
            ["Protein powder", "Whey", "W-1", "line 3"],
        )


class TestNordicConventionsVoecExcludedGoods(unittest.TestCase):
    def test_food_supplement_in_a_voec_shipment(self):
        self.assertListEqual(
            _advise(voec.voec_excluded_goods, T_SHIRT, PROTEIN_POWDER),
            [
                dict(
                    code=EXCLUDED_GOODS,
                    level="warning",
                    message=(
                        "This VOEC shipment to Norway carries Protein powder (foodstuffs). "
                        "VOEC does not cover foodstuffs, goods requiring an import permit, or excise goods, "
                        "so the consignment must be split or the whole shipment declared at the border "
                        "with VAT collected on import."
                    ),
                    details=dict(
                        plugin="advisor_nordic_conventions",
                        lane="SE-NO",
                        sources=EXCLUDED_GOODS_SOURCES,
                        lines=[1],
                        classes=["foodstuffs"],
                    ),
                )
            ],
        )

    def test_wine_in_a_voec_shipment_on_dhl(self):
        messages = _advise(
            voec.voec_excluded_goods, WINE, carrier="dhl_freight_sweden", service=DHL_PARCEL_CONNECT
        )

        self.assertListEqual(_codes(messages), [EXCLUDED_GOODS])
        self.assertListEqual(messages[0]["details"]["classes"], ["alcohol"])

    def test_live_plant_in_a_voec_shipment(self):
        messages = _advise(voec.voec_excluded_goods, OLIVE_TREE)

        self.assertListEqual(messages[0]["details"]["classes"], ["restricted"])
        self.assertIn("Olive tree (restricted)", messages[0]["message"])

    def test_item_named_by_its_sku(self):
        messages = _advise(voec.voec_excluded_goods, VITAMINS_BY_SKU)

        self.assertListEqual(messages[0]["details"]["classes"], ["pharmaceuticals"])
        self.assertIn("VIT-100 (pharmaceuticals)", messages[0]["message"])

    def test_several_excluded_items_are_listed_in_order(self):
        messages = _advise(voec.voec_excluded_goods, WINE, T_SHIRT, PROTEIN_POWDER)

        self.assertIn("carries Wine (alcohol), Protein powder (foodstuffs).", messages[0]["message"])
        self.assertListEqual(messages[0]["details"]["lines"], [0, 2])
        self.assertListEqual(messages[0]["details"]["classes"], ["alcohol", "foodstuffs"])

    def test_animal_feed_is_not_a_foodstuff(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, DOG_FOOD), [])

    def test_beeswax_is_not_a_foodstuff(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, BEESWAX), [])

    def test_commodity_without_an_hs_code(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, UNCODED_CHOCOLATE), [])

    def test_no_voec_number(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, PROTEIN_POWDER, voec_number=None), [])

    def test_voec_number_to_another_destination(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, PROTEIN_POWDER, recipient="CH"), [])

    def test_recipient_in_svalbard(self):
        self.assertListEqual(_advise(voec.voec_excluded_goods, PROTEIN_POWDER, recipient="NO_SVALBARD"), [])



class TestNordicConventionsVoecItemOverThreshold(unittest.TestCase):
    def test_item_at_nok_3000(self):
        self.assertListEqual(
            _advise(voec.voec_item_over_threshold, _valued(3000, "NOK")),
            [
                dict(
                    code=ITEM_OVER_THRESHOLD,
                    level="warning",
                    message=(
                        "This VOEC shipment to Norway carries Road bike, each with a unit value at or above NOK 3,000. "
                        "VOEC applies per item below NOK 3,000, excluding shipping and insurance, "
                        "and an item at or above it goes through ordinary import declaration, "
                        "so the consignment must be split or the whole shipment declared at the border."
                    ),
                    details=dict(
                        plugin="advisor_nordic_conventions",
                        lane="SE-NO",
                        sources=[
                            sources.SKE_VOEC_PER_ITEM_THRESHOLD.to_dict(),
                            sources.SKE_VOEC_MIXED_CONSIGNMENT.to_dict(),
                            sources.TOLL_VOEC_PER_ITEM_THRESHOLD.to_dict(),
                            sources.MVAF_LOW_VALUE_GOODS.to_dict(),
                            sources.NORGES_BANK_RATES.to_dict(),
                            *SVALBARD_SOURCES,
                        ],
                        lines=[0],
                        rate_date="2026-10-15",
                    ),
                )
            ],
        )

    def test_item_just_below_nok_3000(self):
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(2999, "NOK")), [])

    def test_item_clearly_over_in_sek_on_dhl(self):
        messages = _advise(
            voec.voec_item_over_threshold,
            _valued(5000, "SEK"),
            carrier="dhl_freight_sweden",
            service=DHL_PARCEL_CONNECT,
        )

        self.assertListEqual(_codes(messages), [ITEM_OVER_THRESHOLD])

    def test_converted_item_inside_the_margin(self):
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(285, "EUR")), [])
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(295.71, "EUR")), [])

    def test_converted_item_past_the_margin(self):
        self.assertListEqual(
            _codes(_advise(voec.voec_item_over_threshold, _valued(296, "EUR"))), [ITEM_OVER_THRESHOLD]
        )

    def test_converted_item_exactly_at_the_margin_limit(self):
        # No table rate converts a finite decimal amount to exactly NOK 3,150,
        # so the rate is patched to one that does.
        with mock.patch.dict(rates.NOK_PER_UNIT, {"SEK": decimal.Decimal("0.9")}):
            self.assertTrue(voec.at_or_above_limit(models.Commodity(**_valued(3500, "SEK"))))
            self.assertFalse(voec.at_or_above_limit(models.Commodity(**_valued(3499.99, "SEK"))))
            self.assertListEqual(
                _codes(_advise(voec.voec_item_over_threshold, _valued(3500, "SEK"))), [ITEM_OVER_THRESHOLD]
            )

    def test_several_units_below_the_limit(self):
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(2000, "NOK", quantity=3)), [])

    def test_only_items_over_the_limit_are_listed(self):
        messages = _advise(
            voec.voec_item_over_threshold,
            _valued(200, "SEK", description="Bell"),
            _valued(5000, "DKK", description="Frame"),
            _commodity(sku="WHEEL-1", value_amount=400, value_currency="USD"),
        )

        self.assertIn("carries Frame, WHEEL-1, each", messages[0]["message"])
        self.assertListEqual(messages[0]["details"]["lines"], [1, 2])

    def test_currency_outside_the_table(self):
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(5000, "GBP")), [])

    def test_item_without_a_value_or_currency(self):
        self.assertListEqual(
            _advise(
                voec.voec_item_over_threshold,
                _valued(0, "NOK"),
                _commodity(description="Unvalued", value_amount=None, value_currency="NOK"),
                _commodity(description="No currency", value_amount=5000, value_currency=None),
            ),
            [],
        )

    def test_recipient_in_jan_mayen(self):
        self.assertListEqual(
            _advise(voec.voec_item_over_threshold, _valued(5000, "NOK"), recipient="NO_JAN_MAYEN"), []
        )

    def test_no_voec_number(self):
        self.assertListEqual(_advise(voec.voec_item_over_threshold, _valued(5000, "NOK"), voec_number=None), [])



class TestNordicConventionsVoecBusinessRecipient(unittest.TestCase):
    def test_recipient_with_an_organisation_number(self):
        self.assertListEqual(
            _advise(voec.voec_business_recipient, T_SHIRT, recipient="NO_TAXED"),
            [
                dict(
                    code=BUSINESS_RECIPIENT,
                    level="warning",
                    message=(
                        "This VOEC shipment to Norway goes to a recipient with a tax id. "
                        "VOEC covers sales to consumers only, and a business buyer self-assesses the VAT, "
                        "so VOEC VAT must not be charged."
                    ),
                    details=dict(
                        plugin="advisor_nordic_conventions",
                        lane="SE-NO",
                        sources=[
                            sources.SKE_VOEC_B2B.to_dict(),
                            sources.SKE_VOEC_B2C_ONLY.to_dict(),
                            sources.MVAL_LOW_VALUE_EXCLUSIONS.to_dict(),
                            *SVALBARD_SOURCES,
                        ],
                    ),
                )
            ],
        )

    def test_recipient_with_a_state_tax_id_on_dhl(self):
        messages = _advise(
            voec.voec_business_recipient,
            T_SHIRT,
            recipient="NO_STATE_TAXED",
            carrier="dhl_freight_sweden",
            service=DHL_PARCEL_CONNECT,
        )

        self.assertListEqual(_codes(messages), [BUSINESS_RECIPIENT])

    def test_consumer_recipient(self):
        self.assertListEqual(_advise(voec.voec_business_recipient, T_SHIRT), [])

    def test_blank_tax_ids_read_as_a_consumer(self):
        request = fixture.shipment(
            "SE",
            "NO",
            "postnord_parcel",
            customs=fixture.customs("merchandise", True, voec_number=VOEC_NUMBER),
        )
        request.recipient.federal_tax_id = " "
        request.recipient.state_tax_id = ""

        self.assertListEqual(fixture.messages(voec.voec_business_recipient, request, fixture.context("postnord")), [])

    def test_business_recipient_in_svalbard(self):
        self.assertListEqual(
            _advise(
                voec.voec_business_recipient,
                T_SHIRT,
                recipient="NO_SVALBARD_TAXED",
                carrier="dhl_freight_sweden",
                service=DHL_PARCEL_CONNECT,
            ),
            [],
        )

    def test_business_recipient_without_a_voec_number(self):
        self.assertListEqual(
            _advise(voec.voec_business_recipient, T_SHIRT, recipient="NO_TAXED", voec_number=None), []
        )


if __name__ == "__main__":
    unittest.main()

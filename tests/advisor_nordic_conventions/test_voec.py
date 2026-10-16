import unittest

import karrio.plugins.advisor_nordic_conventions.rules.voec as voec
from . import fixture

VOEC_NUMBER = "VOEC2024001"


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


if __name__ == "__main__":
    unittest.main()

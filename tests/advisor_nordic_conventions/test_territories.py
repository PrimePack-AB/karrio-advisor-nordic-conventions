import typing
import unittest

import karrio.plugins.advisor_nordic_conventions.territories as territories
from . import fixture


# Known finding, tracked as a follow-up to the PostNord connector's customs-correctness
# work and out of scope for openspec/changes/align-connector-claims: karrio-postnord's
# NON_EU_VAT_POSTAL_RANGES omits FR 97000-97999, DK 3800-3999, FR 98600-98899, and
# EL 63086. The cross-check expects exactly this difference, so any other divergence,
# or the connector adding these ranges, fails it.
KNOWN_MISSING_CONNECTOR_RANGES: typing.Dict[str, typing.FrozenSet[typing.Tuple[str, int, int]]] = {
    "postnord": frozenset(
        {
            ("FR", 97000, 97999),
            ("DK", 3800, 3999),
            ("FR", 98600, 98899),
            ("EL", 63086, 63086),
        }
    ),
}


class TestNordicConventionsTerritories(unittest.TestCase):
    def test_greece_is_inside(self):
        self.assertTrue(territories.in_eu_vat_area("GR", "10431"))

    def test_aland_by_country_code_is_outside(self):
        self.assertFalse(territories.in_eu_vat_area("AX", "22100"))

    def test_aland_by_postal_code_is_outside(self):
        self.assertFalse(territories.in_eu_vat_area("FI", "22100"))

    def test_canary_islands_by_postal_code_is_outside(self):
        self.assertFalse(territories.in_eu_vat_area("ES", "35 001"))

    def test_mainland_spain_is_inside(self):
        self.assertTrue(territories.in_eu_vat_area("ES", "28001"))

    def test_non_numeric_postal_code_falls_back_to_country(self):
        self.assertFalse(territories.in_eu_vat_area("NO", "N-0150"))

    def test_postal_code_prefixes_are_normalised_before_checks(self):
        cases = (
            ("FI", "FI-22100", False),
            ("FI", "fi 22100", False),
            ("FI", "FI22100", False),
            ("FI", "FI 22 100", False),
            ("FI", " FI - 22100 ", False),
            ("FI", "AX-22100", False),
            ("FI", "AX 22100", False),
            ("FI", "AX22100", False),
            ("FI", "FI-00100", True),
            ("DK", "DK 3800", False),
            ("DK", "DK-3900", False),
            ("DK", "GL-3900", False),
            ("DK", "FO-3800", False),
            ("ES", "ES-35001", False),
            ("ES", "IC-35001", False),
            ("ES", "EA-51001", False),
            ("SE", "AX-22100", True),
            ("MT", "MTF 1234", True),
            ("GB", "GB-BT1 1AA", True),
            ("GB", "gb bt1 1aa", True),
            ("GB", "BT1 1AA", True),
            ("GB", "GB-EC1A 1BB", False),
            ("GB", "GBBT1 1AA", False),
            ("GB", "JE2 3AB", False),
            ("GB", "GY1 1AA", False),
            ("GB", "IM1 1AA", False),
        )
        self.assertListEqual(
            [
                (country_code, postal_code, territories.in_eu_vat_area(country_code, postal_code))
                for country_code, postal_code, _ in cases
            ],
            list(cases),
        )

    def test_prefix_codes_of_a_country(self):
        self.assertDictEqual(
            {country_code: territories.postal_prefix_codes(country_code) for country_code in ("FI", "DK", "ES", "GB", "JE", "")},
            dict(FI=("FI", "AX"), DK=("DK", "FO", "GL"), ES=("ES", "IC", "EA"), GB=("GB",), JE=(), **{"": ()}),
        )

    def test_monaco_is_inside(self):
        self.assertTrue(territories.in_eu_vat_area("MC", "98000"))

    def test_france_with_monaco_postal_code_is_inside(self):
        self.assertTrue(territories.in_eu_vat_area("FR", "98000"))

    def test_northern_ireland_by_postal_prefix_is_inside(self):
        self.assertTrue(territories.in_eu_vat_area("GB", "BT1 1AA"))

    def test_great_britain_is_outside(self):
        self.assertFalse(territories.in_eu_vat_area("GB", "EC1A 1BB"))

    def test_mount_athos_by_postal_code_is_outside(self):
        self.assertListEqual(
            [
                territories.in_eu_vat_area("GR", "630 86"),
                territories.in_eu_vat_area("EL", "630 86"),
                territories.in_eu_vat_area("EL", "10431"),
            ],
            [False, False, True],
        )

    def test_french_pacific_collectivities_by_postal_code_are_outside(self):
        self.assertListEqual(
            [
                territories.in_eu_vat_area("FR", postal_code)
                for postal_code in ("98000", "98599", "98600", "98713", "98800", "98899", "98900")
            ],
            [True, True, False, False, False, False, True],
        )

    def test_french_overseas_departments_by_postal_code_are_outside(self):
        self.assertListEqual(
            [
                territories.in_eu_vat_area("FR", postal_code)
                for postal_code in ("96999", "97000", "97100", "97400", "97600", "97999", "98000")
            ],
            [True, False, False, False, False, False, True],
        )

    def test_faroe_islands_and_greenland_by_danish_postal_code_are_outside(self):
        self.assertListEqual(
            [
                territories.in_eu_vat_area("DK", postal_code)
                for postal_code in ("3799", "3800", "3900", "3999", "4000")
            ],
            [True, False, False, False, True],
        )

    def test_faroe_islands_and_greenland_by_territory_prefix_or_faroese_format_are_outside(self):
        cases = (
            ("DK", "FO-100", False),
            ("DK", "fo 100", False),
            ("DK", "FO100", False),
            ("DK", "FO 3800", False),
            ("DK", "GL 3900", False),
            ("DK", "GL-1000", False),
            ("DK", "gl2100", False),
            ("DK", "100", False),
            ("DK", "DK-100", False),
            ("DK", "dk 999", False),
            ("DK", "1 00", False),
            ("DK", "1000", True),
            ("DK", "DK-2100", True),
            ("DK", "0100", True),
            ("DK", "10", True),
            ("DK", "10000", True),
            ("FO", "100", False),
            ("GL", "3900", False),
            ("SE", "FO-100", True),
            ("SE", "100", True),
            ("FI", "100", True),
        )
        self.assertListEqual(
            [
                (country_code, postal_code, territories.in_eu_vat_area(country_code, postal_code))
                for country_code, postal_code, _ in cases
            ],
            list(cases),
        )

    def test_matches_connector_tables(self):
        for carrier_name in ("postnord", "dhl_freight_sweden"):
            with self.subTest(carrier_name=carrier_name):
                units = fixture.connector_units(self, carrier_name)
                known_missing = KNOWN_MISSING_CONNECTOR_RANGES.get(carrier_name, frozenset())

                self.assertSetEqual(
                    set(territories.EU_VAT_AREA_COUNTRIES),
                    set(units.EU_VAT_AREA_COUNTRIES),
                )
                self.assertTupleEqual(
                    tuple(
                        postal_range
                        for postal_range in territories.NON_EU_VAT_POSTAL_RANGES
                        if postal_range not in known_missing
                    ),
                    units.NON_EU_VAT_POSTAL_RANGES,
                    msg=(
                        f"the {carrier_name} connector is expected to omit exactly {sorted(known_missing)}; "
                        "if it now lists them, remove them from KNOWN_MISSING_CONNECTOR_RANGES"
                        if known_missing
                        else None
                    ),
                )
                self.assertTupleEqual(
                    territories.EU_VAT_POSTAL_PREFIXES,
                    units.EU_VAT_POSTAL_PREFIXES,
                )


if __name__ == "__main__":
    unittest.main()

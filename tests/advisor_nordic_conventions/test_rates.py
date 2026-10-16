import decimal
import unittest

import karrio.plugins.advisor_nordic_conventions.rates as rates


class TestNordicConventionsRates(unittest.TestCase):
    def test_per_100_quotes_are_stored_per_unit(self):
        self.assertEqual(rates.to_nok(100, "SEK"), decimal.Decimal("95.31"))
        self.assertEqual(rates.to_nok(100, "DKK"), decimal.Decimal("142.5"))

    def test_per_unit_quotes_convert_directly(self):
        self.assertEqual(rates.to_nok(285, "EUR"), decimal.Decimal("3035.82"))
        self.assertEqual(rates.to_nok(1, "USD"), decimal.Decimal("9.5039"))
        self.assertEqual(rates.to_nok(3000, "NOK"), decimal.Decimal("3000"))

    def test_currency_is_read_case_insensitively(self):
        self.assertEqual(rates.to_nok(100, "sek"), decimal.Decimal("95.31"))

    def test_currency_outside_the_table_is_not_converted(self):
        self.assertIsNone(rates.to_nok(5000, "GBP"))
        self.assertIsNone(rates.to_nok(5000, None))

    def test_table_date_limit_and_margin(self):
        self.assertEqual(rates.RATE_DATE, "2026-10-15")
        self.assertEqual(rates.VOEC_LIMIT_NOK, decimal.Decimal("3000"))
        self.assertEqual(rates.MARGIN, decimal.Decimal("1.05"))
        self.assertSetEqual(set(rates.NOK_PER_UNIT), {"SEK", "EUR", "DKK", "USD", "NOK"})


if __name__ == "__main__":
    unittest.main()

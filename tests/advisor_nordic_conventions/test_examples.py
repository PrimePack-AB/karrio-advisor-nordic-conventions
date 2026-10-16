"""The runnable shipment examples under ``examples/``."""

import unittest

import karrio.references as references
from examples import voec_parcels_to_norway


class TestExamples(unittest.TestCase):
    def tearDown(self):
        references.import_extensions()

    def test_voec_parcels_to_norway_yield_their_voec_advisories(self):
        voec_parcels_to_norway.load_plugin()

        self.assertListEqual(
            [
                (
                    title,
                    [
                        message.code
                        for message in voec_parcels_to_norway.advise(request)
                        if "_voec_" in message.code
                    ],
                )
                for title, request in voec_parcels_to_norway.SCENARIOS
            ],
            [
                ("(a) food supplement, HS 2106.90", ["advisor_nordic_conventions_voec_excluded_goods"]),
                ("(b) NOK 3,200 item", ["advisor_nordic_conventions_voec_item_over_threshold"]),
                ("(c) SEK 3,400 item", ["advisor_nordic_conventions_voec_item_over_threshold"]),
                ("(d) recipient with a tax id", ["advisor_nordic_conventions_voec_business_recipient"]),
                ("(e) Svalbard recipient (9171)", []),
                ("(f) consumer, clean, under the limit", []),
            ],
        )


if __name__ == "__main__":
    unittest.main()

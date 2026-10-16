import unittest

from karrio.plugins.advisor_nordic_conventions.codes import AdvisoryClassification


class TestNordicConventionsCodes(unittest.TestCase):
    def test_twenty_six_classifications_follow_the_namespace_rule(self):
        self.assertEqual(len(AdvisoryClassification), 26)
        self.assertListEqual(
            [
                classification
                for classification in AdvisoryClassification
                if not classification.value.startswith("advisor_nordic_conventions_")
            ],
            [],
        )

    def test_voec_applicability_classifications(self):
        self.assertListEqual(
            [
                AdvisoryClassification.voec_excluded_goods.value,
                AdvisoryClassification.voec_item_over_threshold.value,
                AdvisoryClassification.voec_business_recipient.value,
            ],
            [
                "advisor_nordic_conventions_voec_excluded_goods",
                "advisor_nordic_conventions_voec_item_over_threshold",
                "advisor_nordic_conventions_voec_business_recipient",
            ],
        )


if __name__ == "__main__":
    unittest.main()

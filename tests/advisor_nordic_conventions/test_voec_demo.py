import importlib.util
import pathlib
import unittest

import karrio.references as references

DEMO = pathlib.Path(__file__).resolve().parents[2] / "examples" / "voec_demo.py"


def _load_demo():
    spec = importlib.util.spec_from_file_location("voec_demo", DEMO)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestVoecDemo(unittest.TestCase):
    def tearDown(self):
        references.import_extensions()

    def test_each_scenario_yields_its_voec_advisories(self):
        demo = _load_demo()
        demo.load_plugin()

        self.assertListEqual(
            [
                (title, [message.code for message in demo.advise(request) if "_voec_" in message.code])
                for title, request in demo.SCENARIOS
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

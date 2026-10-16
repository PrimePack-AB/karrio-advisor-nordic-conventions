"""Run the VOEC applicability advisories through karrio's own plugin discovery.

The plugin is loaded from its installed ``karrio.plugins`` entry point by
``karrio.references.import_extensions``, and each SE to NO PostNord shipment
request is advised by ``karrio.core.advisors.run_advisors``, the runner that
``karrio.Shipment.create`` calls once a carrier has returned shipment details.

Run from the repository root with an interpreter that has the plugin and the
forked karrio SDK installed:

    .venv/bin/python examples/voec_demo.py
"""

import typing

import attr
import karrio.core.advisors as advisors
import karrio.core.models as models
import karrio.core.settings as settings
import karrio.lib as lib
import karrio.references as references

PLUGIN_ID = "advisor_nordic_conventions"
VOEC_NUMBER = "VOEC2024001"

SHIPPER = dict(
    company_name="Nordic Outdoor AB",
    address_line1="Drottninggatan 1",
    postal_code="11122",
    city="Stockholm",
    country_code="SE",
)
OSLO_CONSUMER = dict(
    person_name="Kari Nordmann",
    address_line1="Karl Johans gate 1",
    postal_code="0150",
    city="Oslo",
    country_code="NO",
)
OSLO_BUSINESS = dict(OSLO_CONSUMER, company_name="Nordmann Sport AS", federal_tax_id="912345678")
LONGYEARBYEN_CONSUMER = dict(
    person_name="Ola Nordmann",
    address_line1="Vei 230",
    postal_code="9171",
    city="Longyearbyen",
    country_code="NO",
)


@attr.s(auto_attribs=True)
class PostNordConnection(settings.Settings):
    """The non-secret part of a PostNord connection; advisors only see its name and id."""

    @property
    def carrier_name(self) -> str:
        return "postnord"


def _item(description: str, amount: float, currency: str, hs_code: str = "6211.43") -> dict:
    return dict(
        description=description,
        hs_code=hs_code,
        quantity=1,
        weight=0.5,
        weight_unit="KG",
        value_amount=amount,
        value_currency=currency,
        origin_country="SE",
    )


def _request(recipient: dict, *items: dict) -> models.ShipmentRequest:
    return lib.to_object(
        models.ShipmentRequest,
        lib.to_dict(
            dict(
                service="postnord_parcel",
                shipper=SHIPPER,
                recipient=recipient,
                parcels=[dict(weight=1.0, weight_unit="KG")],
                customs=dict(
                    content_type="merchandise",
                    commercial_invoice=True,
                    commodities=list(items),
                    options=dict(voec_number=VOEC_NUMBER),
                ),
            )
        ),
    )


SCENARIOS: typing.List[typing.Tuple[str, models.ShipmentRequest]] = [
    (
        "(a) food supplement, HS 2106.90",
        _request(OSLO_CONSUMER, _item("Protein powder", 349.0, "SEK", hs_code="2106.90")),
    ),
    ("(b) NOK 3,200 item", _request(OSLO_CONSUMER, _item("Road bike", 3200.0, "NOK"))),
    ("(c) SEK 3,400 item", _request(OSLO_CONSUMER, _item("Rain jacket", 3400.0, "SEK"))),
    ("(d) recipient with a tax id", _request(OSLO_BUSINESS, _item("Rain jacket", 899.0, "SEK"))),
    (
        "(e) Svalbard recipient (9171)",
        _request(
            LONGYEARBYEN_CONSUMER,
            _item("Protein powder", 349.0, "SEK", hs_code="2106.90"),
            _item("Road bike", 3200.0, "NOK"),
        ),
    ),
    ("(f) consumer, clean, under the limit", _request(OSLO_CONSUMER, _item("Rain jacket", 899.0, "SEK"))),
]


def advise(request: models.ShipmentRequest) -> typing.List[models.Message]:
    """The plugin's messages for one shipment request, as karrio's runner returns them."""
    return [
        message
        for message in advisors.run_advisors(request, PostNordConnection(carrier_id="postnord_se"), "shipping")
        if (message.details or {}).get("plugin") == PLUGIN_ID
    ]


def load_plugin() -> None:
    """Load installed karrio plugins and fail unless this one registered advisors."""
    references.import_extensions()

    if not any(plugin_id == PLUGIN_ID for plugin_id, _ in references.get_advisors()):
        raise SystemExit(f"karrio discovered no advisors from {PLUGIN_ID}; is the plugin installed?")


def _render(message: models.Message) -> str:
    sources = "\n".join(
        f"      [{source['tag']}] {source['reference']}" for source in message.details.get("sources", [])
    )
    code = getattr(message.code, "value", message.code)
    return f"  {message.level}  {code}\n    {message.message}\n    sources:\n{sources}"


def main() -> None:
    load_plugin()
    plugin = references.collect_references(plugin_registry={})["plugins"][PLUGIN_ID]
    print(f"karrio plugin {PLUGIN_ID} loaded via entry point, type {plugin['type']}")

    for title, request in SCENARIOS:
        messages = advise(request)
        voec = [message for message in messages if "_voec_" in message.code]
        print(f"\n== {title}: {len(voec)} VOEC advisories, {len(messages)} advisories in all")
        print("\n".join(_render(message) for message in messages) or "  (none)")


if __name__ == "__main__":
    main()

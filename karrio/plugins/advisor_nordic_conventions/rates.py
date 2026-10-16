"""Exchange rates the VOEC per-item threshold advisory converts commodity values with.

One rate per currency in NOK per unit, from Norges Bank's EXR dataset (spot,
ECB concertation time 14:15 CET) for ``RATE_DATE``, retrieved 2026-10-16 from
``sources.NORGES_BANK_EXR_URL``. Norges Bank quotes SEK and DKK per 100 units
(``UNIT_MULT`` 2); they are stored here per unit. A refresh replaces the rates
and ``RATE_DATE`` together and updates the URL constant's annotation and its
footnote.
"""

import decimal
import typing

RATE_DATE = "2026-10-15"

NOK_PER_UNIT: typing.Dict[str, decimal.Decimal] = {
    "SEK": decimal.Decimal("0.9531"),
    "EUR": decimal.Decimal("10.652"),
    "DKK": decimal.Decimal("1.425"),
    "USD": decimal.Decimal("9.5039"),
    "NOK": decimal.Decimal("1.0"),
}

VOEC_LIMIT_NOK = decimal.Decimal("3000")

# A design choice, not a sourced fact: the seller may convert at any rate
# published within 30 days before payment, so a converted value fires only
# when it clears the limit by this factor.
MARGIN = decimal.Decimal("1.05")


def to_nok(amount: typing.Any, currency: typing.Optional[str]) -> typing.Optional[decimal.Decimal]:
    """The amount in NOK at the table rate, or None for a currency outside the table."""
    rate = NOK_PER_UNIT.get(str(currency or "").upper())
    return None if rate is None else decimal.Decimal(str(amount)) * rate

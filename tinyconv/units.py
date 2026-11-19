"""Unit tables and conversion.

Every unit maps to its category's base unit:  base = value * factor + offset.
Converting from A to B goes through the base:  B.from_base(A.to_base(value)).
"""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Unit:
    symbol: str
    name: str
    category: str
    factor: float
    offset: float = 0.0

    def to_base(self, value: float) -> float:
        return value * self.factor + self.offset

    def from_base(self, value: float) -> float:
        return (value - self.offset) / self.factor


UNITS = [
    # length, base: metre
    Unit("m", "metre", "length", 1.0),
    Unit("km", "kilometre", "length", 1000.0),
    Unit("cm", "centimetre", "length", 0.01),
    Unit("mm", "millimetre", "length", 0.001),
    Unit("in", "inch", "length", 0.0254),
    Unit("ft", "foot", "length", 0.3048),
    Unit("yd", "yard", "length", 0.9144),
    Unit("mi", "mile", "length", 1609.344),
    # mass, base: kilogram
    Unit("kg", "kilogram", "mass", 1.0),
    Unit("g", "gram", "mass", 0.001),
    Unit("lb", "pound", "mass", 0.45359237),
    Unit("oz", "ounce", "mass", 0.028349523125),
    # volume, base: litre
    Unit("L", "litre", "volume", 1.0),
    Unit("mL", "millilitre", "volume", 0.001),
    Unit("m3", "cubic metre", "volume", 1000.0),
    Unit("gal", "US gallon", "volume", 3.785411784),
    Unit("cup", "US cup", "volume", 0.2365882365),
    Unit("floz", "US fluid ounce", "volume", 0.0295735295625),
    # temperature, base: kelvin
    Unit("K", "kelvin", "temperature", 1.0),
    Unit("C", "degree Celsius", "temperature", 1.0, 273.15),
    Unit("F", "degree Fahrenheit", "temperature", 5 / 9, 273.15 - 32 * 5 / 9),
]

BY_SYMBOL = {u.symbol: u for u in UNITS}


class UnitError(ValueError):
    """An unknown unit, or units from different categories."""


def get_unit(symbol: str) -> Unit:
    try:
        return BY_SYMBOL[symbol]
    except KeyError:
        raise UnitError(f"unknown unit: {symbol}") from None


def convert(value: float, src: str, dst: str) -> float:
    a, b = get_unit(src), get_unit(dst)
    if a.category != b.category:
        raise UnitError(f"can't convert {a.category} ({a.symbol}) to {b.category} ({b.symbol})")
    return b.from_base(a.to_base(value))


def categories() -> list[str]:
    return sorted({u.category for u in UNITS})


def as_json_data() -> dict:
    """The unit table for the web page (web/units.json)."""
    return {"units": [asdict(u) for u in UNITS]}

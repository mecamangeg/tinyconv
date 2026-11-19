import itertools
import math
import unittest

from tinyconv import units


class KnownValues(unittest.TestCase):
    def check(self, value, src, dst, expected):
        self.assertTrue(
            math.isclose(units.convert(value, src, dst), expected, rel_tol=1e-12, abs_tol=1e-9),
            f"{value} {src} -> {dst}: got {units.convert(value, src, dst)}, want {expected}",
        )

    def test_length(self):
        self.check(1, "mi", "km", 1.609344)
        self.check(12, "in", "ft", 1)
        self.check(1, "yd", "cm", 91.44)

    def test_mass(self):
        self.check(1, "lb", "g", 453.59237)
        self.check(16, "oz", "lb", 1)

    def test_volume(self):
        self.check(1, "m3", "L", 1000)
        self.check(1, "L", "mL", 1000)
        self.check(1, "gal", "L", 3.785411784)
        self.check(1, "gal", "cup", 16)
        self.check(1, "cup", "mL", 236.5882365)
        self.check(1, "cup", "floz", 8)
        self.check(1, "floz", "mL", 29.5735295625)
        self.check(128, "floz", "gal", 1)

    def test_temperature(self):
        self.check(100, "C", "F", 212)
        self.check(-40, "F", "C", -40)
        self.check(0, "K", "C", -273.15)


class Table(unittest.TestCase):
    def test_symbols_unique(self):
        symbols = [u.symbol for u in units.UNITS]
        self.assertEqual(len(symbols), len(set(symbols)))

    def test_each_category_has_one_base_unit(self):
        for cat in units.categories():
            base = [u for u in units.UNITS if u.category == cat and u.factor == 1 and u.offset == 0]
            self.assertEqual(len(base), 1, cat)

    def test_round_trip_every_pair(self):
        for a, b in itertools.permutations(units.UNITS, 2):
            if a.category != b.category:
                continue
            back = units.convert(units.convert(3.5, a.symbol, b.symbol), b.symbol, a.symbol)
            self.assertTrue(math.isclose(back, 3.5, rel_tol=1e-12), f"{a.symbol} <-> {b.symbol}")


class Errors(unittest.TestCase):
    def test_unknown_unit(self):
        with self.assertRaises(units.UnitError):
            units.convert(1, "parsec", "m")

    def test_different_categories(self):
        with self.assertRaisesRegex(units.UnitError, "can't convert length"):
            units.convert(1, "m", "kg")


if __name__ == "__main__":
    unittest.main()

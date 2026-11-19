import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from tinyconv import units
from tinyconv.__main__ import main

ROOT = Path(__file__).resolve().parent.parent


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class Cli(unittest.TestCase):
    def test_convert(self):
        code, out, _ = run("5", "km", "mi")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "5 km = 3.10686 mi")

    def test_unknown_unit_exits_2(self):
        code, _, err = run("1", "furlong", "m")
        self.assertEqual(code, 2)
        self.assertIn("unknown unit: furlong", err)

    def test_missing_arguments(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            main(["5", "km"])

    def test_export_json(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "units.json")
            code, _, _ = run("--export-json", path)
            self.assertEqual(code, 0)
            self.assertEqual(json.load(open(path)), units.as_json_data())


class WebTable(unittest.TestCase):
    def test_web_units_json_is_current(self):
        """web/units.json must match the table: run `make web` after changing units."""
        with open(ROOT / "web" / "units.json", encoding="utf-8") as f:
            self.assertEqual(json.load(f), units.as_json_data())


if __name__ == "__main__":
    unittest.main()

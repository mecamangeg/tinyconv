"""Command line:  python3 -m tinyconv 5 km mi"""
import argparse
import difflib
import json
import sys

from . import units


def resolve(text: str) -> str:
    """Map a unit symbol or (case-insensitive) name to its symbol, or raise UnitError."""
    if text in units.BY_SYMBOL:
        return text
    by_name = {u.name.lower(): u.symbol for u in units.UNITS}
    if text.lower() in by_name:
        return by_name[text.lower()]
    pool = {}
    for u in units.UNITS:
        pool.setdefault(u.symbol.lower(), u.symbol)
        pool.setdefault(u.name.lower(), u.name)
    close = difflib.get_close_matches(text.lower(), list(pool), n=3)
    msg = f"unknown unit: {text}"
    if close:
        msg += f" (did you mean {', '.join(pool[c] for c in close)}?)"
    raise units.UnitError(msg)


def print_units() -> None:
    for cat in units.categories():
        print(f"{cat}:")
        for u in units.UNITS:
            if u.category == cat:
                print(f"  {u.symbol:<3} {u.name}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tinyconv", description="Convert a value between units.")
    p.add_argument("value", nargs="?", type=float, help="the number to convert")
    p.add_argument("src", nargs="?", help="the unit it is in, for example km")
    p.add_argument("dst", nargs="?", help="the unit to convert to, for example mi")
    p.add_argument("--export-json", metavar="FILE", help="write the unit table for the web page and exit")
    p.add_argument("--list", action="store_true", help="list the units by category and exit")
    args = p.parse_args(argv)

    if args.list:
        print_units()
        return 0

    if args.export_json:
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(units.as_json_data(), f, indent=2)
            f.write("\n")
        return 0
    if args.value is None or args.src is None or args.dst is None:
        p.error("give VALUE FROM TO, for example: 5 km mi")

    try:
        src, dst = resolve(args.src), resolve(args.dst)
        result = units.convert(args.value, src, dst)
    except units.UnitError as e:
        print(f"tinyconv: {e}", file=sys.stderr)
        return 2
    print(f"{args.value:g} {src} = {result:.6g} {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

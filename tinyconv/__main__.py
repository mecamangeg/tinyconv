"""Command line:  python3 -m tinyconv 5 km mi"""
import argparse
import json
import sys

from . import units


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tinyconv", description="Convert a value between units.")
    p.add_argument("value", nargs="?", type=float, help="the number to convert")
    p.add_argument("src", nargs="?", help="the unit it is in, for example km")
    p.add_argument("dst", nargs="?", help="the unit to convert to, for example mi")
    p.add_argument("--export-json", metavar="FILE", help="write the unit table for the web page and exit")
    args = p.parse_args(argv)

    if args.export_json:
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(units.as_json_data(), f, indent=2)
            f.write("\n")
        return 0
    if args.value is None or args.src is None or args.dst is None:
        p.error("give VALUE FROM TO, for example: 5 km mi")

    try:
        result = units.convert(args.value, args.src, args.dst)
    except units.UnitError as e:
        print(f"tinyconv: {e}", file=sys.stderr)
        return 2
    print(f"{args.value:g} {args.src} = {result:.6g} {args.dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

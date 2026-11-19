# tinyconv

A small unit converter: a Python command line and a web page that share one unit table.
Standard library only, no dependencies.

It is the coder-lab's practice project, used to exercise the lab's workspace, preview, backup and
background-agent features. It holds no personal or sensitive data.

## Use

```sh
python3 -m tinyconv 5 km mi        # 5 km = 3.10686 mi
python3 -m tinyconv 100 C F        # 100 C = 212 F
python3 -m tinyconv 5 kilometre mile   # unit names work too, in any case
python3 -m tinyconv --list         # list the units, grouped by category
```

Units can be given as a symbol (case-sensitive, e.g. `km`, `C`) or as a name (case-insensitive,
e.g. `Kilometre`). An unknown unit exits with code 2 and suggests close matches:
`tinyconv: unknown unit: kms (did you mean km?)`.

The web page lives in `web/`. Serve that folder (`make serve`, then open http://localhost:8080).

## Units

| Category | Units |
|---|---|
| length | m, km, cm, mm, in, ft, yd, mi |
| mass | kg, g, lb, oz |
| volume | L, mL, m3, gal, cup, floz |
| temperature | K, C, F |

Every unit maps to its category's base unit: `base = value * factor + offset`.

## Develop

```sh
make test     # the unit tests
make web      # rewrite web/units.json after changing the unit table
```

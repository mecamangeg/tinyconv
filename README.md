# tinyconv

A small unit converter: a Python command line and a web page that share one unit table.
Standard library only, no dependencies.

It is the coder-lab's practice project, used to exercise the lab's workspace, preview, backup and
background-agent features. It holds no personal or sensitive data.

## Use

```sh
python3 -m tinyconv 5 km mi        # 5 km = 3.10686 mi
python3 -m tinyconv 100 C F        # 100 C = 212 F
```

The web page lives in `web/`. Serve that folder (`make serve`, then open http://localhost:8080).

## Units

| Category | Units |
|---|---|
| length | m, km, cm, mm, in, ft, yd, mi |
| mass | kg, g, lb, oz |
| temperature | K, C, F |

Every unit maps to its category's base unit: `base = value * factor + offset`.

## Develop

```sh
make test     # the unit tests
make web      # rewrite web/units.json after changing the unit table
```

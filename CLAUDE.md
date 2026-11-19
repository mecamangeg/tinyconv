# tinyconv

- Python standard library only. Don't add dependencies.
- The unit table is `tinyconv/units.py`. After changing it, run `make web` so `web/units.json`
  matches; a test checks this.
- Run `make test` before every commit, and commit only when it passes.
- Use exact definitions for unit factors (for example 1 in = 0.0254 m), never rounded ones.
- Keep the README's unit list in step with the table.

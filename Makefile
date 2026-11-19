.PHONY: test web serve

test:
	python3 -m unittest discover -s tests -t . -v

web:
	python3 -m tinyconv --export-json web/units.json

serve:
	python3 -m http.server 8080 --bind 127.0.0.1 --directory web

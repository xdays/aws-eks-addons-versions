.PHONY: all install fetch generate serve clean

all: fetch generate

install:
	pip install -r requirements.txt

fetch:
	python scripts/fetch_addons.py

generate:
	python scripts/generate_html.py

serve:
	cd output && python -m http.server 8000

clean:
	rm -f output/addons_data.json output/index.html

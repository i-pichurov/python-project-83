PORT ?= 8000

install:
	poetry install --sync

lint:
	poetry run flake8

test:
	poetry run pytest -vv tests

check: test lint

dev:
	poetry run flask --app page_analyzer.app --debug run --port $(PORT)

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app
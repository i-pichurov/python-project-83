PORT ?= 8000

install:
	uv sync

lint:
	uv run flake8 --exclude .venv,__pycache__,migrations

test:
	uv run pytest -vv tests

check: test lint

dev:
	uv run flask --app page_analyzer.app --debug run --port $(PORT)

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app
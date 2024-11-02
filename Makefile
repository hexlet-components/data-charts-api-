PORT ?= 4000

install:
	uv sync

dev:
	uv run fastapi dev app/server.py --host 0.0.0.0 --port $(PORT)

run:
	uv run uvicorn --workers 4 --host 0.0.0.0 --port $(PORT) app.server:app

build:
	docker build . --tag=data-charts-api

start:
	-docker stop data-charts-api || true
	-docker rm data-charts-api || true
	docker run -d --name data-charts-api -p $(PORT):$(PORT) data-charts-api

stop:
	-docker stop data-charts-api || true

rm:
	-docker rm data-charts-api || true

bash:
	docker run --rm -it data-charts-api bash

test:
	uv run pytest

lint:
	uv run ruff check .

check: lint

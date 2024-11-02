PORT ?= 4000

install:
	uv sync

dev:
	uv run flask --app app.server run --debug -h 0.0.0.0 -p $(PORT)

run:
	uv run gunicorn -w 4 -b 0.0.0.0:$(PORT) app.server:app

build:
	docker build . --tag=data-charts-api

start:
	-docker stop data-charts-api
	-docker rm data-charts-api
	docker run -d --name data-charts-api -p $(PORT):$(PORT) data-charts-api

stop:
	-docker stop data-charts-api

rm:
	-docker rm data-charts-api

bash:
	docker run --rm -it data-charts-api bash

test:
	uv run pytest

lint:
	uv run ruff check .

check: lint

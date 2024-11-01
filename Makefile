PORT ?= 4000

install:
	uv sync

dev:
	uv run flask --app app.server run --debug -h 0.0.0.0 -p $(PORT)

run:
	uv run gunicorn -w 4 -b 0.0.0.0:$(PORT) app.server:app

start:
	make stop rm || true
	docker run -p $(PORT):$(PORT) data-charts-api make run

build:
	docker build . --tag=data-charts-api

stop:
	docker stop data-charts-api

rm:
	docker rm data-charts-api

bash:
	docker run --rm -it data-charts-api bash

PID_FILE = server.pid

test:
	env PORT=$(PORT) DATABASE_URL=postgres://student:student@65.108.223.44:5432/chartsdb \
	make dev & echo $$! > $(PID_FILE) && \
	sleep 2 && \
	uv run pytest; \
	status=$$?; \
	if [ -f $(PID_FILE) ]; then kill `cat $(PID_FILE)` && rm $(PID_FILE); fi; \
	exit $$status

lint:
	uv run ruff check .

check: test lint

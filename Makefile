PORT ?= 4000

install:
	uv sync

dev:
	uv run fastapi dev app/server.py --host 0.0.0.0 --port $(PORT)

run:
	uv run uvicorn --workers 4 --host 0.0.0.0 --port $(PORT) app.server:app

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
	sleep 1; \
	exit $$status

lint:
	uv run ruff check .

check: test lint

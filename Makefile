PORT ?= 4000

install:
	poetry install

dev:
	poetry run flask  --app app.server run --debug -h 0.0.0.0 -p $(PORT)

run:
	poetry run gunicorn -w 4 -b 0.0.0.0:$(PORT) app.server:app

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

dev:
	poetry run flask  --app app.server run --debug -h 0.0.0.0 -p 3000

run:
	poetry run gunicorn -w 4 -b 0.0.0.0:3000 app.server:app

start:
	make stop rm || true
	docker run -p 3000:3000 data-charts-api make run

build:
	docker build . -t data-charts-api

stop:
	docker stop data-charts-api

rm:
	docker rm data-charts-api

bash:
	docker run --rm -it data-charts-api bash

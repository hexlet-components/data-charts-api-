dev:
	poetry run flask  --app app.server run --debug -h 0.0.0.0 -p 3000

run:
	poetry run gunicorn -w 4 -b 0.0.0.0:3000 app.server:app

start:
	make stop rm || true
	docker run -p 3000:3000 app-chartsdb make run

build:
	docker build . -t app-chartsdb

stop:
	docker stop app-chartsdb

rm:
	docker rm app-chartsdb

bash:
	docker run --rm -it app-chartsdb bash

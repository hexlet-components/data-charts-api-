start:
	make stop rm || true
	docker run -it \
		-p 5432:5432 \
		-e POSTGRES_PASSWORD=password \
		--name data-chartsdb \
		data-chartsdb

build:
	docker build . -t data-chartsdb

stop:
	docker stop data-chartsdb

rm:
	docker rm data-chartsdb

bash:
	docker run --rm -it data-chartsdb bash

compose:
	docker compose up

compose-down:
	docker compose down -v --remove-orphans

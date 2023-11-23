FROM postgres:latest

WORKDIR /scripts

COPY db/data_generator/data /scripts/data
COPY setup_user.sql /scripts/
COPY scripts/ /scripts/db


RUN cat /scripts/db/*.sql > /tmp/chartsdb.sql

RUN echo "createdb chartsdb" >> /docker-entrypoint-initdb.d/run.sh
RUN echo "psql -d chartsdb -U postgres -f /tmp/chartsdb.sql" >> /docker-entrypoint-initdb.d/run.sh
RUN echo "psql -d chartsdb -U postgres -f /scripts/setup_user.sql" >> /docker-entrypoint-initdb.d/run.sh

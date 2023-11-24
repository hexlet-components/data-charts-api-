FROM python:slim

RUN apt-get update && apt-get install -yqq make
RUN pip install poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true


WORKDIR /app
COPY . .
RUN poetry install

CMD ["make run"]

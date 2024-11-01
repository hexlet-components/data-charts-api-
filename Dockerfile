FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y make && \
    pip install uv

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
RUN --mount=type=cache,target=/root/.cache/uv

WORKDIR /app
COPY . .
RUN make install

CMD ["make", "run"]

FROM python:3.7.2-slim-stretch

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        make \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir \
        pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY . .

RUN make build && python database/migrations/init.py

CMD ["pipenv", "run", "serve"]

EXPOSE 50051

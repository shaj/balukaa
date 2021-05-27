FROM python:3.9-buster

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /var/app

# RUN pip install uvicorn gunicorn

RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-dev

COPY balukaa .

# RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["bash", "./entrypoint.sh"]

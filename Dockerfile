FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
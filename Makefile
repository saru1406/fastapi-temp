setup:
	docker compose up -d --build
	@make up
	docker compose exec app alembic upgrade head

shell:
	docker compose exec app bash

build:
	docker compose up -d --build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose exec app alembic upgrade head

fresh:
	docker compose exec app alembic downgrade base
	docker compose exec app alembic upgrade head

history:
	docker compose exec app alembic history

format:
	docker-compose exec app black .
	docker-compose exec app isort .

log:
	docker logs fastapi-temp-app-1

poetry-install:
	docker compose exec app poetry install

poetry-show:
	docker compose exec app poetry show

secrets:
	docker compose exec app python script.py
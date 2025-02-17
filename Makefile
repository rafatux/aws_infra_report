# Makefile

.PHONY: install run test lint format clean

install:
	poetry install

run:
	poetry run python infra_report/main.py --profile dev --output informe_aws.md

format:
	poetry run black infra_report/

lint:
	poetry run flake8 infra_report/

test:
	poetry run pytest tests/

clean:
	rm -rf .mypy_cache .pytest_cache .tox dist build
	find . -name __pycache__ -exec rm -rf {} 
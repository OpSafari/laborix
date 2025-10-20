.PHONY: build test format-check format lint test-all typecheck release

build:
	.venv/bin/python -m build --wheel --no-isolation

test:
	.venv/bin/python -m pytest -q -m "not slow"

format-check:
	.venv/bin/ruff format --check src tests examples scripts
	.venv/bin/ruff check src tests examples scripts

format:
	.venv/bin/ruff check --fix src tests examples scripts
	.venv/bin/ruff format src tests examples scripts

lint:
	.venv/bin/ruff check src tests examples scripts

test-all:
	.venv/bin/python -m pytest -q

typecheck:
	.venv/bin/mypy

release: format-check lint typecheck test-all
	.venv/bin/python -m build --no-isolation

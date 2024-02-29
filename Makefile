.PHONY: cicd_setup install test check_style check_format

cicd_setup:
	@echo "Installing Poetry..."
	@python3 -m pip install poetry
	@poetry config virtualenvs.in-project true

install:
	@echo "Installing dependencies with Poetry..."
	@poetry install

test:
	@echo "Running tests..."
	@poetry run pytest -o log_cli=true --log-cli-level=DEBUG

check_style:
	@echo "Checking style with ruff..."
	@poetry run ruff check .

check_format:
	@echo "Checking formatting with ruff..."
	@poetry run ruff format --check

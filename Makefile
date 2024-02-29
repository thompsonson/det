.PHONY: cicd_setup install

cicd_setup:
	@echo "Installing Poetry..."
	@python3 -m pip install poetry
	@poetry config virtualenvs.in-project true

install:
	@echo "Installing dependencies with Poetry..."
	@poetry install

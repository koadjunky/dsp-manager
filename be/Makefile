install:
	poetry install

lock:
	poetry lock --no-update

black:  # run the black formatter
	poetry run black $(ARGS) ./

isort: # run isort
	poetry run isort $(ARGS) ./

flake: # run autoflake
	poetry run autoflake --in-place --recursive --ignore-init-module-imports --remove-unused-variables --remove-all-unused-imports ./

mypy:
	poetry run mypy --no-site-packages --ignore-missing-imports --no-strict-optional ./

format: flake black isort mypy # run all formatters at once

format_check:
	poetry run python -m black --check ./
	poetry run python -m isort --check ./
	poetry run python -m autoflake --check --recursive --ignore-init-module-imports --remove-unused-variables --remove-all-unused-imports ./
	poetry run mypy --no-site-packages --ignore-missing-imports --no-strict-optional ./

vulture:
	poetry run python -m vulture src/

test: # run tests with PYTHONPATH set to root dict
	poetry run python -m pytest src/

run:
	rm test.db
	poetry run uvicorn dsp_be.main:app --reload --port 8000 --reload-dir="src"


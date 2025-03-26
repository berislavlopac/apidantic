# List available recipes.
help:
    @just --list --unsorted

# Run unit tests.
test:
    uv run pytest --spec

# Run unit tests with coverage report.
test-with-coverage:
    uv run pytest --spec --cov

# Run linting and formating checks.
lint:
    uv run ruff format --check .
    uv run ruff check .

# Run static typing analysis.
type:
    uv run mypy --install-types --non-interactive

# Run all checks.
check: lint type

# Reformat the code using isort and ruff.
[confirm]
reformat:
    uv run ruff format .
    uv run ruff check --select I --fix .

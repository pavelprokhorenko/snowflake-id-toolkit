MYPY_COMMAND ?= dmypy run

fmt:
	uv run ruff format

lint:
	uv run ruff check
	uv run $(MYPY_COMMAND) -- .
	uv lock --check

test:
	uv run pytest --numprocesses logical --dist worksteal

test-cov:
	uv run pytest --numprocesses logical --dist worksteal --cov --cov-report=term-missing --cov-report=xml

test-cov-html:
	uv run pytest --numprocesses logical --dist worksteal --cov --cov-report=term-missing --cov-report=xml --cov-report=html

MYPY_COMMAND ?= dmypy run

fmt:
	uv run ruff format

lint:
	uv run ruff check
	uv run $(MYPY_COMMAND) -- .
	uv lock --check

test:
	uv run pytest --numprocesses logical --dist worksteal

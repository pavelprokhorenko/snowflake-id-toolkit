# Register all fixtures by importing their modules
pytest_plugins = [
    "tests.fixtures.common",
    "tests.fixtures.configs",
    "tests.fixtures.generators",
    "tests.fixtures.ids",
]

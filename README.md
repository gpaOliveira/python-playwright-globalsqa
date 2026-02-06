# python-playwright-globalsqa
Automated UI tests using Python and Playwright


## Project setup ⚙️

In this project we use [Poetry](https://python-poetry.org/) and [Pyenv](https://github.com/pyenv/pyenv), so follow these steps to setup it:

```bash

# 1. Install Poetry and Pyenv:
curl -sSL https://install.python-poetry.org | python3 -
curl -fsSL https://pyenv.run | bash
# or, with Homebrew  (macOS):
# brew install poetry
# brew install pyenv

# 2. Verify installation and make sure we are using Python 3.12.6:
poetry --version
poetry env use 3.12.6
poetry install

# 3. Create or enter the project virtual environment:
eval $(poetry env activate)

# 4. Install browsers:
playwright install

# 5. Run tests:
poetry run pytest

# 6. (Optional) If ruff (our linter), black (our formatter), or isort (our importer sorter) failed, reformat with:
./scripts/fix.sh
```

## Tooling & Reporting ✨

We strive for fast, repeatable, and readable test runs with built-in tooling:

- **Lint & Format**: `ruff`, `black`, and `isort` are configured for the project to keep code consistent and fast to check. They are executed automatically when running `poetry run pytest`.
- **Logging**: Pytest is configured to emit structured CLI logs during runs (timestamped, INFO level) so debugging test failures is quick.
- **HTML Reports**: `pytest-html` produces a single self-contained report (see `reports/report.html`) including embedded screenshots and logging lines.

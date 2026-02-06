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

- **Lint & Format**: `ruff`, `black`, and `isort` are configured for the project to keep code consistent and fast to check. They are executed automatically when running `poetry run pytest`. If they fail, [a script](./scripts/fix.sh) can be used to trigger automatic fixes
- **Logging**: Pytest is configured to emit structured CLI logs during runs (timestamped, INFO level) so debugging test failures is quick.
- **HTML Reporting**: `pytest-html` produces a single self-contained report (see `reports/report.html`) including embedded screenshots and logging lines.
- **CI ready**: We use Docker to ensure consistent and reproducible environments for our testing. Our [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml) files are configured to build and run the tests and export the HTML report. Scripts to help bring it [up](./scripts/docker-run.sh) and [down](./scripts/docker-stop.sh) are also available. We also leverage GitHub Actions for continuous integration, showcasing the HTML report in the Pull Request.


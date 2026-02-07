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

# 6. (Optional) If ruff (our linter), black (our formatter), or isort (our importer sorter) failed, reformat manually with:
# This is not often needed, as `poetry run pytest` already checks and fix the issues
./scripts/fix.sh

# 7. (Optional) In case you don't want to install all these python stuff, run with docker using
./scripts/docker-up.sh
```

## Tooling & Reporting ✨

We strive for fast, repeatable, and readable test runs with built-in tooling:

- **Lint & Format**: `ruff`, `black`, and `isort` are configured for the project to keep code consistent and fast to check. They are executed automatically when running `poetry run pytest`. If they fail, [a script](./scripts/fix.sh) can be used to trigger automatic fixes
- **Logging**: Pytest is configured to emit structured CLI logs during runs (timestamped, INFO level) so debugging test failures is quick.
- **HTML Reporting**: `pytest-html` produces a single self-contained report including embedded screenshots and logging lines. Check your `reports/` folder after running tests, there should be a HTML file there with the timestamp of your execution.
- **CI ready**: We also use Docker to ensure consistent and reproducible browser environments for our testing - so even if you don't have Python in your machine you can run the tests! Our [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml) files are configured to build and run the tests and export the HTML report. Scripts to help bring it [up](./scripts/docker-run.sh) and [down](./scripts/docker-stop.sh) are also available. We also leverage GitHub Actions for continuous integration, showcasing the HTML report in the Pull Request.


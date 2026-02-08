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

# 6. Debug tests (remember to add a pdb.set_trace() somewhere!):
# This may be useful to do when debugging: self.page.screenshot(path="screenshot.png", full_page=True)
poetry run pytest --pdb

# 7. (Optional) If ruff (our linter), black (our formatter), or isort (our importer sorter) failed, reformat manually with:
# This is not often needed, as `poetry run pytest` already checks and fix the issues
./scripts/fix.sh

# 8. (Optional) In case you don't want to install all these python stuff, run with docker using
./scripts/docker-up.sh
```

## Tooling & Reporting ✨

We strive for fast, repeatable, and readable test runs with built-in tooling:

- **Lint & Format**: `ruff`, `black`, and `isort` are configured for the project to keep code consistent and fast to check. They are executed automatically when running `poetry run pytest`. If they fail, [a script](./scripts/fix.sh) can be used to trigger automatic fixes
- **Logging**: Pytest is configured to emit structured CLI logs during runs (timestamped, INFO level) so debugging test failures is quick.
- **HTML Reporting**: `pytest-html` produces a single self-contained report including embedded screenshots and logging lines. Check your `reports/` folder after running tests, there should be a HTML file there with the timestamp of your execution. Such report already brings snapshots (taken by our page objects) and a video of your test.
- **CI ready**: We also use Docker to ensure consistent and reproducible browser environments for our testing - so even if you don't have Python in your machine you can run the tests! Our [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml) files are configured to build and run the tests and export the HTML report. Scripts to help bring it [up](./scripts/docker-run.sh) and [down](./scripts/docker-stop.sh) are also available. We also leverage GitHub Actions for continuous integration, showcasing the HTML report in the Pull Request.

## Page Objects 🛠️

The classes in [pages folder](./tests/pages/) mirror how the application under test is used in order to simplify the amount of entry points available for tests.

Therefore, tests interact initially with either:
* [LoginCustomer](./tests/pages/customer/LoginCustomer.py) with the fixture `login_customer` if they need to perform operations as a customer, such as checking their balance, withdraw, or deposit money
* [LoginManager](./tests/pages/manager/LoginManager.py) with the fixture `login_manager` if they need to perform operations as a manager, such as adding managing customers or accounts.

From each of those pages, with special navigation method, the other page objects are acquired. For example, when calling `LoginCustomer.login(...)`, the page object `DetailsCustomers` is returned so that the test can interaxt with it to (among other things) withdraw money from the account.

The full list of available page objects is summarised below per folder (all part of [pages folder](./tests/pages/)):

- On [base folder](./tests/pages/base/) one finds common helpers, such as:
    - [Login](./tests/pages/base/Login.py): the base class for both LoginCustomer and LoginManager, wrapping up the logic to access the BASE_URL.
    - [Reporter](./tests/pages/base/Reporter.py): used by other page objects to add information (such as log lines or images) to the final HTML report.

- On [customer folder](./tests/pages/customer/) one finds page objects related to flows for customers, as follows:
    - [LoginCustomer](./tests/pages/customer/LoginCustomer.py): the main class for tests to login as a customer, with calls wrapping up the navigation to DetailsCustomer
    - [DetailsCustomer](./tests/pages/customer/DetailsCustomer.py): allow tests (after login as a customer was done) to deposit or withdraw money and see the transactions on an account

- On [manager folder](./tests/pages/manager/) one finds page objects related to flows for managers, as follows:
    - [LoginManager](./tests/pages/manager/LoginManager.py): the main class for tests to login as a manager, with calls wrapping up the navigation to the others
    - [AddCustomer](./tests/pages/manager/AddCustomer.py): allow tests to add a customer (after login as a manager was done)
    - [ListCustomers](./tests/pages/manager/ListCustomers.py): allow tests to list and delete customers (after login as a manager was done)
    - [OpenAccount](./tests/pages/manager/OpenAccount.py): allow tests to open an account for a customer (after login as a manager was done)

## Test cases 🧪

With Python and Playwright, end to end (e2e) tests were created and placed under the [tests folder](./tests/e2e/) to care for specific integation risks, as follows:

1. **test_login_as_customer**: ensures that an existing customer can log in and logout, mainly to make sure we have our common data in our test environment

2. **test_deposit_withdraw_customer**: TBD, ensures that a customer can deposit, then withdraw, and see all the transactions in their account

3. **test_manager_create_customer**: a manager can create a customer, without an account, and that customer can login

4. **test_manager_create_customer_with_account**: a manager can create a customer with an account (with any currency), and that customer can login. Also, they cannot withdraw money from their account (since they have no money in it).

5. **test_manager_create_customer_then_delete**: a manager can create a customer and then delete it. As part of that process, they can filter the customers.

Given those tests are end-to-end, they're not meant to be exhaustive. They assume some checks (the ones tied to single page behaviours) were already created as **frontend unit tests**, as follow:
- Add customer mandatory fields and validations
- Currency options (Dollar, Pound, Rupee)
- Search/filtering behaviour when listing customer (first name works, last name works, post code works, first name + last name does not, check customers with same name but different last name to see if two rows appear)
- All customer's data is shown (possible bug: Account Number is not shown for newly added customers)
- All customer's data can be sorted (by first name, by last name, by post code, not by account number)
- Filter customer's transactions by date-time (possible bug: I'm _almost_ sure this doesn't stops working when we clear both start/end dates and try to set them again)
- Sort customer's transactions by date-time (not by amount nor transaction type, apparently)

Similarly, all those tests assume some **API tests** were made to tests similar behaviours only using the involved microservices, as follows:
- Add customer mandatory fields and validations
- Creation of manager account (and login as one)
- Creation of customers can't be made if not using a manager token
- Currency options (Dollar, Pound, Rupee) are the same in all schemas
- Search/filtering behaviour when listing customer
- Customer's data can be retrieved (only by someone with a manager token),filtered, and deleted

## Future 🔮

Ideas to expand the current work include:

- **Review ruff/black rules**: the default served us well so far, but we can streghten it more (e.g. force docstrings)
- **Retry tests (x3)**: since the application is in another place, it can happen that the navigation to it fails, so retrying tests automatically may be enough to increase our confidence in tests
- **Mermaid Diagram for Pages**: the pages folder explanation can probably be extracted to an entity relationship diagram, with comments
- **Expand e2e test cases**: some missing tests were deliberately left behind for the sake of time, as follows:
    - Home button _always_ leading the user to the main login screen, regardless where the user is
    - Add multiple accounts to a customer, so they can manage their balance individually (and check balances are different)
    - Reset transactions on an account, cleaning up all the data and setting the balance to 0
- **WebVitals**: Try [WebVitals](https://web.dev/articles/vitals) integration with Playwright in Python.
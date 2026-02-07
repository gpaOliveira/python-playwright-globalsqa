import logging
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import pytest_html
from pages.LoginCustomer import LoginCustomer
from pages.LoginManager import LoginManager
from pages.Reporter import Reporter
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    expect,
    sync_playwright,
)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    browser: Browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, base_url: str):
    context: BrowserContext = browser.new_context(
        base_url=base_url, record_video_dir="reports/videos/"
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    page: Page = context.new_page()
    page.set_default_timeout(3_000)  # 3s
    page.set_default_navigation_timeout(3_000)  # 3s
    yield page
    page.close()


@pytest.fixture()
def logger() -> logging.Logger:
    logger = logging.getLogger("MainLogger")
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture()
def reporter(page: Page, logger: logging.Logger, extras) -> Reporter:
    return Reporter(page, logger, extras)


@pytest.fixture()
def login_customer(page: Page, reporter: Reporter) -> LoginCustomer:
    return LoginCustomer(page, reporter)


@pytest.fixture()
def login_manager(page: Page, reporter: Reporter) -> LoginManager:
    return LoginManager(page, reporter)


def pytest_configure(config):
    # Add some more metadata to the HTML report
    config._metadata = getattr(config, "_metadata", {})
    config._metadata.setdefault("Platform", sys.platform)

    # Set default values for tests
    # (In the future we can use dotenv or a config file for these)
    config.option.base_url = (
        "https://www.globalsqa.com/angularJs-protractor/BankingProject/#"
    )
    config.option.verify_base_url = True
    expect.set_options(timeout=1_000)  # 1s

    # set custom report name with datetime if not already set by command line
    if not config.option.htmlpath:
        now = datetime.now()
        # create report target dir
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        # custom report file
        report = reports_dir.joinpath(f"report_{now.strftime('%Y%m%d_%H%M%S')}.html")
        # adjust plugin options
        config.option.htmlpath = report
        config.option.self_contained_html = True


def _run_cmd(cmd):
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.returncode, proc.stdout.decode(errors="replace")
    except FileNotFoundError:
        return None, f"{cmd[0]} not found"


def pytest_sessionstart(session):
    """Fix lint/format before tests start."""
    # Leaving as a comment here in case we _only_ want to check for issues, not fix them
    # checks = [
    #     ("ruff", ["ruff", "check", "."]),
    #     ("isort", ["isort", "--check-only", "."]),
    #     ("black", ["black", "--check", "."]),
    # ]
    checks = [
        ("ruff", ["ruff", "check", ".", "--fix"]),
        ("ruff", ["ruff", "check", "."]),
        ("isort", ["isort", "."]),
        ("isort", ["isort", "--check-only", "."]),
        ("black", ["black", "."]),
        ("black", ["black", "--check", "."]),
    ]

    failures = []
    for name, cmd in checks:
        if shutil.which(cmd[0]) is None:
            # tool not installed — skip but warn
            try:
                session.config.warn(
                    "C1", f"{name} not installed; skipping {name} check"
                )
            except Exception:
                print(f"{name} not installed; skipping {name} check")
            continue
        rc, out = _run_cmd(cmd)
        if rc != 0:
            failures.append((name, out))

    if failures:
        msg_parts = [f"{name} failed:\n{out}" for name, out in failures]
        pytest.exit("\n\n".join(msg_parts), returncode=1)


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return datetime.now().timestamp()


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.__dict__.get('description')}</td>")
    cells.insert(1, f'<td class="col-time">{datetime.now(timezone.utc)}</td>')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # https://github.com/microsoft/playwright-pytest/issues/121
    # https://pytest-html.readthedocs.io/en/latest/user_guide.html#enhancing-reports
    # https://pytest-html.readthedocs.io/en/latest/user_guide.html#modifying-the-results-table
    outcome = yield
    report = outcome.get_result()
    report.description = item.function.__doc__
    extra = getattr(report, "extras", [])
    if report.when == "call":
        if "page" in item.funcargs:
            page: Page = item.funcargs["page"]
            Reporter(
                page=page,
                logger=item.funcargs.get("logger"),
                extras=extra,
            ).snapshot()
            extra.append(
                pytest_html.extras.url(
                    content=str(
                        Path(page.video.path()).relative_to(
                            Path.cwd().joinpath("reports")
                        )
                    ),
                    name="Video",
                )
            )

        report.extras = extra

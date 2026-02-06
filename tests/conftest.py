import logging
import shutil
import subprocess
import sys
from base64 import b64encode

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture()
def logger():
    logger = logging.getLogger("MainLogger")
    logger.setLevel(logging.INFO)
    return logger


def pytest_configure(config):
    # Add some more metadata to the HTML report
    config._metadata = getattr(config, "_metadata", {})
    config._metadata.setdefault("Platform", sys.platform)


def _run_cmd(cmd):
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.returncode, proc.stdout.decode(errors="replace")
    except FileNotFoundError:
        return None, f"{cmd[0]} not found"


def pytest_sessionstart(session):
    """Run lint/format checks before tests start."""
    checks = [
        ("ruff", ["ruff", "check", "."]),
        ("isort", ["isort", "--check-only", "."]),
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extras", [])
    if report.when == "call":
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            img_bytes = page.screenshot()
            img_b64 = b64encode(img_bytes).decode("ascii")
            extra.append(pytest_html.extras.png(img_b64))
        report.extras = extra

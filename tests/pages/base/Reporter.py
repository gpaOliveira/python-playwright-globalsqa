import logging
from base64 import b64encode
from typing import List

import pytest_html
from playwright.sync_api import Page


class Reporter:

    def __init__(self, page: Page, logger: logging.Logger, extras: List):
        self.page = page
        self.logger = logger
        self.extras = extras

    def log(self, message):
        self.logger.info(message)

    def log_with_snapshot(self, message):
        self.log(message)
        self.snapshot()

    def snapshot(self):
        img_bytes = self.page.screenshot()
        img_b64 = b64encode(img_bytes).decode("ascii")
        self.extras.append(pytest_html.extras.png(img_b64))

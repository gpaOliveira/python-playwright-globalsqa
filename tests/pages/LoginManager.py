from playwright.sync_api import Page

from .Login import Login
from .Reporter import Reporter


class LoginManager(Login):
    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page, reporter)

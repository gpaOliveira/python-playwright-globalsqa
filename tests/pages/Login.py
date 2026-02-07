from playwright.sync_api import Locator, Page, expect

from .Reporter import Reporter


class Login:
    def __init__(self, page: Page, reporter: Reporter):
        self.page = page
        self.reporter = reporter
        self.home_button: Locator = self.page.get_by_role("button", name="Home")
        self.manager_button: Locator = self.page.get_by_role(
            "button", name="Bank Manager Login"
        )
        self.customer_button: Locator = self.page.get_by_role(
            "button", name="Customer Login"
        )

    def navigate(self):
        self.reporter.log("Navigating to BASE_URL/login")
        self.page.goto("#/login")
        self.reporter.log_with_snapshot(self.page.url)
        expect(self.manager_button).to_be_visible()
        expect(self.customer_button).to_be_visible()

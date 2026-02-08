from pages.base.Currency import Currency
from pages.base.Reporter import Reporter
from playwright.sync_api import Locator, Page, expect


class OpenAccount:
    """Page object to handle the navigation to open an account to a customer, which is done by a manager."""

    def __init__(self, page: Page, reporter: Reporter):
        self.page = page
        self.reporter = reporter
        self.open_account_button: Locator = self.page.get_by_role(
            "button", name="Open Account"
        )
        self.customer_select: Locator = self.page.locator("#userSelect")
        self.currency_select: Locator = self.page.locator("#currency")
        self.process_button: Locator = self.page.get_by_role("button", name="Process")

    def navigate(self):
        """
        Navigates to the login manager page to add a new customer.

        **WARNING:** Assumes we are already logged in as a manager.
        """
        self.reporter.log_with_snapshot("Navigating as a manager to add a new customer")
        self.open_account_button.click()
        self._expect_new_account_default_values()

    def _expect_new_account_default_values(self):
        """
        Verifies that the new account form has the expected default values.
        """
        expect(self.customer_select).to_have_value("")
        expect(self.currency_select).to_have_value("")
        expect(self.process_button).to_be_visible()

    def open_account(self, customer_full_name: str, currency: Currency):
        """
        Open a new account for a customer with full name and currency as specified as inputs.

        Also ensures that the form is empty before filling it in and submitting as well as after submitting.

        **WARNING:** Assumes self.navigate() was called before it

        Args:
            customer_full_name (str): The customer full name (first name and last name).
            currency (Currency): The currency to use
        """
        self.reporter.log_with_snapshot(
            "Adding a new customer with the following details:  "
            f"Full Name: {customer_full_name}, Currency: {currency}"
        )
        self.customer_select.select_option(label=customer_full_name)
        self.currency_select.select_option(label=currency.value)
        self.process_button.click()
        self._expect_new_account_default_values()

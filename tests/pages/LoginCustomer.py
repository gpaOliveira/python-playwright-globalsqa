from typing import List, Optional

from playwright.sync_api import Page, expect

from .Login import Login
from .Reporter import Reporter


class LoginCustomer(Login):
    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page, reporter)

    def _navigate_login_customer(self):
        self.reporter.log_with_snapshot("Performing login as customer")
        self.customer_button.click()
        expect(self.customer_select).to_be_visible()

    def _select_login_customer(
        self, label: Optional[str] = None, index: Optional[int] = None
    ):
        self.reporter.log_with_snapshot(
            f"Selecting customer with label: {label} and index: {index}"
        )
        check_label = label
        if label is not None and index is None:
            self.customer_select.select_option(label=label)
        if index is not None:
            check_label = self._get_available_customers_to_login()[index]
            self.customer_select.select_option(value=str(index + 1))
        return check_label

    def _click_login_customer(self, check_label: str):
        self.customer_login_button.click()
        self.reporter.log(f"Check if {check_label} is visible after login")
        expect(self.page.get_by_text(f"Welcome {check_label} !!")).to_be_visible()

    def _get_available_customers_to_login(self) -> List[str]:
        expect(self.customer_select).to_be_visible()
        return self.customer_select.all_inner_texts()[0].split("\n")[1:]

    def login(self, label: Optional[str] = None, index: Optional[int] = None):
        self._navigate_login_customer()
        check_label = self._select_login_customer(label, index)
        self._click_login_customer(check_label)

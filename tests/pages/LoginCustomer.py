from typing import List, Optional

from playwright.sync_api import Locator, Page, expect

from .DetailsCustomer import DetailsCustomers
from .Login import Login
from .Reporter import Reporter


class LoginCustomer(Login):
    """Page object to handle the navigation to login as a customer."""

    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page, reporter)
        self.customer_select: Locator = self.page.locator("#userSelect")
        self.login_button: Locator = self.page.get_by_role("button", name="Login")

    def navigate_login_customer(self):
        """
        Navigates to the login page for customers.

        **WARNING:** Assumes .navigate() was called before it
        """
        self.reporter.log_with_snapshot("Performing login as customer")
        self.customer_button.click()
        expect(self.customer_select).to_be_visible()

    def _select_login_customer(
        self, label: Optional[str] = None, index: Optional[int] = None
    ) -> str:
        """
        Selects a customer to login, either with a specific label or by index.

        Args:
            label (Optional[str], optional): The label of the customer to select. Defaults to None.
            index (Optional[int], optional): The index of the customer to select. Defaults to None.
        Returns:
            str: The label of the selected customer.
        """
        self.reporter.log_with_snapshot(
            f"Selecting customer with label: {label} and index: {index}"
        )
        check_label = label
        if label is not None and index is None:
            self.customer_select.select_option(label=label)
        if index is not None:
            check_label = self.get_available_customers_to_login()[index]
            self.customer_select.select_option(value=str(index + 1))
        return check_label

    def _click_login_customer(self, check_label: str):
        """
        Clicks the login button for the selected customer (for which the name was passed as a parameter).

        Asserts that the welcome message for the selected customer is visible.

        Args:
            check_label (str): The label of the customer who logged in.
        """
        self.login_button.click()
        self.reporter.log(f"Check if {check_label} is visible after login")
        expect(self.page.get_by_text(f"Welcome {check_label} !!")).to_be_visible()

    def get_available_customers_to_login(self) -> List[str]:
        """
        Retrieves the list of available customers to login - useful to check when we add/delete customers.

        **WARNING:** Assumes we already clicked the customer login button and are on the screen with the select.

        Returns:
            List[str]: A list of customer labels.
        """
        expect(self.customer_select).to_be_visible()
        return self.customer_select.all_inner_texts()[0].split("\n")[1:]

    def login(
        self, label: Optional[str] = None, index: Optional[int] = None
    ) -> DetailsCustomers:
        """
        Logs in as a customer using the provided label or index.

        Navigates to the login page, selects the customer, and clicks the login button.

        **WARNING:** Assumes self.navigate() was called before it

        Args:
            label (Optional[str], optional): The label of the customer to login. Defaults to None.
            index (Optional[int], optional): The index of the customer to login. Defaults to None.

        Returns:
            DetailsCustomers: A new page object to interact with the details of the logged in customer.
        """
        self.navigate_login_customer()
        check_label = self._select_login_customer(label, index)
        self._click_login_customer(check_label)
        return DetailsCustomers(self.page, self.reporter)

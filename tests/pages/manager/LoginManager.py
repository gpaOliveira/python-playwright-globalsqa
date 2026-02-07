from pages.base.Login import Login
from pages.base.Reporter import Reporter
from playwright.sync_api import Page

from .AddCustomer import AddCustomer
from .ListCustomers import ListCustomers
from .OpenAccount import OpenAccount


class LoginManager(Login):
    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page, reporter)

    def navigate(self):
        """Navigates to the login page for managers."""
        super().navigate()
        self.manager_button.click()

    def navigate_to_add_customer(self) -> AddCustomer:
        """
        Navigates to add a new customer
        Returns:
            CreateNewCustomer: The page object to be used to create a customer.
        """
        self.navigate()
        new_customer = AddCustomer(self.page, self.reporter)
        new_customer.navigate()
        return new_customer

    def navigate_to_open_account(self) -> OpenAccount:
        """
        Navigates to open a new account for a customer.

        Returns:
            OpenAccount: The page object to be used to open an account for a customer.
        """
        self.navigate()
        open_account = OpenAccount(self.page, self.reporter)
        open_account.navigate()
        return open_account

    def navigate_to_list_customers(self) -> ListCustomers:
        """
        Navigates to list customer's data (and maybe delete them).

        Returns:
            ListCostumers: The page object to be used to view customer's data.
        """
        self.navigate()
        list_customers = ListCustomers(self.page, self.reporter)
        list_customers.navigate()
        return list_customers

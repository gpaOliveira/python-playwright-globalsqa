from playwright.sync_api import Page, expect

from .Login import Login
from .Reporter import Reporter


class CreateNewCustomer(Login):
    """Page object to handle the navigation to add a new customer as a manager"""

    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page, reporter)
        self.new_customer = self.page.get_by_role("button", name="Add Customer")
        self.new_customer_first_name = page.get_by_role("textbox", name="First Name")
        self.new_customer_last_name = page.get_by_role("textbox", name="Last Name")
        self.new_customer_post_code = page.get_by_role("textbox", name="Post Code")
        self.new_customer_submit = page.get_by_role("form").get_by_role(
            "button", name="Add Customer"
        )

    def _expect_new_customer_form_empty(self):
        expect(self.new_customer_first_name).to_be_empty()
        expect(self.new_customer_last_name).to_be_empty()
        expect(self.new_customer_post_code).to_be_empty()

    def _navigate_login_manager(self):
        """
        Navigates to the login manager page to add a new customer.

        **WARNING:** Assumes .navigate() was called before it
        """
        self.reporter.log_with_snapshot("Navigating as a manager to add a new customer")
        self.manager_button.click()
        self.new_customer.click()
        self._expect_new_customer_form_empty()

    def _fill_in_customer_detail(self, first_name, last_name, post_code):
        """
        Fills in the details in the new customer form.

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            post_code (str): The post code of the customer.
        """
        self.reporter.log_with_snapshot(
            f"Filling in the new customer form with the following details:  "
            f"First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}"
        )
        self.new_customer_first_name.fill(first_name)
        self.new_customer_last_name.fill(last_name)
        self.new_customer_post_code.fill(post_code)

    def _submit_customer_details(self):
        """
        Submits the details from the new customer form.

        **WARNING**: supposedly a alert/popup/dialog should appear after the new_customer_submit.click(),
        but somehow playwright just ignores it? It works, for now...
        """
        self.reporter.log_with_snapshot("Submitting customer details")
        self.new_customer_submit.click()
        self._expect_new_customer_form_empty()

    def add_customer(self, first_name, last_name, post_code):
        """
        Adds a new customer with the provided details.

        Also ensures that the form is empty before filling it in and submitting as well as after submitting.

        **WARNING:** Assumes .navigate() was called before it

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            post_code (str): The post code of the customer.
        """
        self.reporter.log_with_snapshot(
            "Adding a new customer with the following details:  "
            f"First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}"
        )
        self._navigate_login_manager()
        self._fill_in_customer_detail(first_name, last_name, post_code)
        self._submit_customer_details()

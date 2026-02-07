from playwright.sync_api import Locator, Page, expect

from .Reporter import Reporter


class AddCustomer:
    """Page object to handle the navigation to add a new customer."""

    def __init__(self, page: Page, reporter: Reporter):
        self.page = page
        self.reporter = reporter
        self.new_customer_button: Locator = self.page.get_by_role(
            "button", name="Add Customer"
        )
        self.first_name_input: Locator = page.get_by_role("textbox", name="First Name")
        self.last_name_input: Locator = page.get_by_role("textbox", name="Last Name")
        self.post_code_input: Locator = page.get_by_role("textbox", name="Post Code")
        self.submit_button: Locator = page.get_by_role("form").get_by_role(
            "button", name="Add Customer"
        )

    def navigate(self):
        """
        Navigates to the login manager page to add a new customer.

        **WARNING:** Assumes we are already logged in as a manager.
        """
        self.reporter.log_with_snapshot("Navigating as a manager to add a new customer")
        self.new_customer_button.click()
        self._expect_new_customer_form_empty()

    def _expect_new_customer_form_empty(self):
        """
        Verifies that the new customer form is indeed empty.
        """
        expect(self.first_name_input).to_be_empty()
        expect(self.last_name_input).to_be_empty()
        expect(self.post_code_input).to_be_empty()

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
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.post_code_input.fill(post_code)

    def _submit_customer_details(self):
        """
        Submits the details from the new customer form.

        **WARNING**: supposedly a alert/popup/dialog should appear after the new_customer_submit.click(),
        but somehow playwright just ignores it? It works, for now...
        """
        self.reporter.log_with_snapshot("Submitting customer details")
        self.submit_button.click()
        self._expect_new_customer_form_empty()

    def add_customer(self, first_name, last_name, post_code):
        """
        Adds a new customer with the provided details.

        Also ensures that the form is empty before filling it in and submitting as well as after submitting.

        **WARNING:** Assumes self.navigate() was called before it

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            post_code (str): The post code of the customer.
        """
        self.reporter.log_with_snapshot(
            "Adding a new customer with the following details:  "
            f"First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}"
        )
        self._fill_in_customer_detail(first_name, last_name, post_code)
        self._submit_customer_details()

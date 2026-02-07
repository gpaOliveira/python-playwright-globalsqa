from playwright.sync_api import Locator, Page, expect

from .Reporter import Reporter


class ListCustomers:
    """Page object to handle the listing of customers, allowing a manager to search for them, check their data, and delete them."""

    def __init__(self, page: Page, reporter: Reporter):
        self.page = page
        self.reporter = reporter
        self.customer_list_button: Locator = self.page.get_by_role(
            "button", name="Customers"
        )
        self.search_input: Locator = page.get_by_role("textbox", name="Search Customer")
        self.rows: Locator = self.page.get_by_role("row")

    def navigate(self):
        """
        Navigates to the login manager page to add a new customer.

        **WARNING:** Assumes we are already logged in as a manager.
        """
        self.reporter.log_with_snapshot(
            "Navigating as a manager to list customer's data"
        )
        self.customer_list_button.click()
        expect(self.search_input).to_be_visible()

    def search(self, text: str):
        """
        Search for a customer's information (either their first name, their last name, or their postcode)

        **WARNING:** Assumes self.navigate() was called before it

        Args:
            text (str): The customer's information to search for.
        """
        self.reporter.log_with_snapshot(
            f"Searching for a customer with the following details: {text}"
        )
        self.search_input.clear()
        self.search_input.fill(text)

    def expect_row_data(self, first_name: str, last_name: str, post_code: str):
        """
        Expects a row with the customer's data to be visible.

        **WARNING:** Assumes self.search() was called before it

        Args:
            first_name (str): The customer's first name.
            last_name (str): The customer's last name.
            post_code (str): The customer's post code.
        """
        self.reporter.log_with_snapshot(
            f"Expecting to see a row with the following data: {first_name}, {last_name}, {post_code}"
        )
        expect(self.rows.get_by_role("cell", name=first_name)).to_be_visible()
        expect(self.rows.get_by_role("cell", name=last_name)).to_be_visible()
        expect(self.rows.get_by_role("cell", name=post_code)).to_be_visible()

    def delete_row_index(self, index: int):
        """
        Deletes a row with the customer's data by clicking the delete button in the row.

        Args:
            index (int): The index of the row to delete, starting from 0.
        """
        self.reporter.log_with_snapshot(
            f"Deleting the row with index {index} in the list of customers"
        )
        # Avoid first row, which has the headers
        self.rows.nth(index + 1).get_by_role("button").click()

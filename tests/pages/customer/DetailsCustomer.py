from typing import Literal

from pages.base.Reporter import Reporter
from playwright.sync_api import Locator, Page, expect


class DetailsCustomers:
    """
    Page object to handle the details of a single customers, what they see and what they can do on their page.

    Assumes the customer is already logged in and on the page with their account details.
    """

    def __init__(self, page: Page, reporter: Reporter):
        self.page = page
        self.reporter = reporter
        self.account_select: Locator = self.page.locator("#accountSelect")
        self.transaction_button: Locator = self.page.get_by_role(
            "button", name="Transactions"
        )
        self.deposit_button: Locator = self.page.get_by_role("button", name="Deposit")
        self.withdrawl_button: Locator = self.page.get_by_role(
            "button", name="Withdrawl"
        )
        self.logout_button: Locator = self.page.get_by_role("button", name="Logout")
        self.amount_input: Locator = self.page.get_by_placeholder("amount")
        self.submit_button: Locator = self.page.get_by_role("form").get_by_role(
            "button"
        )

    def logout(self):
        """
        Logs out the customer by clicking the logout button
        """
        self.reporter.log_with_snapshot("Logging out the customer")
        self.logout_button.click()

    def expect_no_account_message(self):
        """
        Expects the message indicating that the customer has no account to be visible.
        """
        self.reporter.log_with_snapshot(
            "Expect customer sees a message to open an account"
        )
        expect(self.page.get_by_text("Please open an account with us")).to_be_visible()

    def expect_account_details(
        self, balance: int, currency: Literal["Dollar", "Pound", "Rupee"]
    ):
        """
        Expects the message indicating that the customer has no account to be visible.
        """
        self.reporter.log_with_snapshot(
            f"Expect customer sees his account balance and currency as {balance} and {currency}"
        )
        expect(
            self.page.get_by_text(f"Balance : {balance} , Currency : {currency}")
        ).to_be_visible()

    def withdraw(self, amount: int):
        """
        Withdraws money from the account.

        Args:
            amount (int): The amount to withdraw.
        """
        self.reporter.log_with_snapshot(f"Withdraw {amount} from the account")
        self.withdrawl_button.click()
        self.amount_input.fill(str(amount))
        self.submit_button.click()

    def expect_withdrawal_error_message(self):
        """
        Expects the error message indicating that the withdrawal cannot be processed to be visible.
        """
        self.reporter.log_with_snapshot(
            "Expect a message indicating that the withdrawal cannot be processed"
        )
        expect(
            self.page.get_by_text(
                "Transaction Failed. You can not withdraw amount more than the balance."
            )
        ).to_be_visible()

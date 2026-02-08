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
        self.back_button: Locator = self.page.get_by_role("button", name="Back")
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

    def deposit(self, amount: int):
        """
        Deposits money on the account.

        Args:
            amount (int): The amount to deposit.
        """
        self.reporter.log_with_snapshot(f"Deposit {amount} on the account")
        self.deposit_button.click()
        self.amount_input.fill(str(amount))
        self.submit_button.click()

    def go_to_transactions(self, expected_count: int = 1, max_count=5):
        """
        Goes to the transactions page by clicking the transactions button.

        BUG: This page is often not showing the rows at all, so we retry some times until we see the amount of rows we expect there.

        **WARNING:** Assumes we are on the account summary page before calling it.

        Args:
            expected_count (int, optional): The amount of rows we expect to see in the transactions page, including the header. Defaults to 1 (so we expect only the header to be seen).
            max_count (int, optional): The maximum amount of times to retry going to the transactions page if we don't see the expected amount of rows. Defaults to 5.
        """
        count = 1
        last_exception = None
        while count <= max_count:
            self.reporter.log_with_snapshot(
                f"Going to the transactions page to see {expected_count} rows (try {count}/{max_count})"
            )
            self.transaction_button.click()
            expect(self.back_button).to_be_visible()
            try:
                # Expect some rows (the header counts as 1)
                expect(self.page.get_by_role("row")).to_have_count(expected_count)
                break
            except AssertionError as exception:
                last_exception = exception
                count += 1
                self.back_button.click()
        if count > max_count:
            raise last_exception

    def expect_transaction_row_contains(
        self, balance: int, transaction_type: Literal["Credit", "Debit"]
    ):
        """
        Expects a row in the transactions table with the given balance and transaction type to be visible.

        Args:
            balance (int): The balance to expect in the transaction row.
            transaction_type (Literal["Credit", "Debit"]): The transaction type to expect in the transaction row.
        """
        self.reporter.log_with_snapshot(
            f"Expect a row in the transactions table with the following details: balance: {balance}, transaction type: {transaction_type}"
        )
        expect(
            self.page.get_by_role("row").filter(
                has_text=f"\t{balance}\t{transaction_type}"
            )
        ).to_be_visible()

    def back_to_account_summary(self):
        """
        Goes back to the account summary page by clicking the transactions button and then going back.

        **WARNING:** Assumes we are on the transactions page before calling it.
        """
        self.reporter.log_with_snapshot("Going back to the account summary page")
        self.back_button.click()

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

    def expect_deposit_successful_message(self):
        """
        Expects the message indicating that the deposit was possible.
        """
        self.reporter.log_with_snapshot(
            "Expect a message indicating that the deposit was possible"
        )
        expect(self.page.get_by_text("Deposit Successful")).to_be_visible()

    def expect_withdrawl_successful_message(self):
        """
        Expects the message indicating that the withdrawl was possible.
        """
        self.reporter.log_with_snapshot(
            "Expect a message indicating that the withdrawl was possible"
        )
        expect(self.page.get_by_text("Transaction successful")).to_be_visible()

from faker import Faker
from pages.base.Currency import Currency
from pages.customer.DetailsCustomer import CustomerMessages
from pages.customer.LoginCustomer import LoginCustomer
from pages.manager.LoginManager import LoginManager


def test_login_and_logout_as_customer(login_customer: LoginCustomer):
    """First customer can login and logout successfully"""

    # Login with first customer
    login_customer.navigate()
    details_page = login_customer.login(index=0)

    # Logout leads us back, seeing the list of customers to login again
    details_page.logout()
    assert [] != login_customer.get_available_customers_to_login()


def test_deposit_withdraw_customer(
    login_manager: LoginManager, faker: Faker, login_customer: LoginCustomer
):
    """
    Ensures that a customer can deposit, then withdraw, and see all the transactions in their account

    BUG: The transactions page is often not showing the rows at all, so we have to
    retry `go_to_transactions` some times until we see the amount of rows we expect in each case.
    """
    first_name = faker.first_name()
    last_name = faker.last_name()
    currency = Currency.POUND

    # Create our customer
    add_customer_page = login_manager.navigate_to_add_customer()
    add_customer_page.add_customer(
        first_name=first_name, last_name=last_name, post_code=faker.postcode()
    )

    # Add an account to our customer
    open_account_page = login_manager.navigate_to_open_account()
    open_account_page.open_account(
        customer_full_name=f"{first_name} {last_name}", currency=currency
    )

    # Check we can login with the newly created customer and see their account summary
    login_customer.navigate()
    details_page = login_customer.login(label=f"{first_name} {last_name}")
    details_page.expect_account_details(balance=0, currency=currency)

    # Check we can deposit money and see the updated account summary
    details_page.deposit(amount=100)
    details_page.expect_account_details(balance=100, currency=currency)
    details_page.expect_message(CustomerMessages.DEPOSIT_SUCCESSFUL)
    details_page.go_to_transactions(expected_count=2)
    details_page.expect_transaction_row_contains(balance=100, transaction_type="Credit")
    details_page.back_to_account_summary()

    # Check we can withdraw money and see the updated account summary
    details_page.withdraw(amount=50)
    details_page.expect_account_details(balance=50, currency=currency)
    details_page.expect_message(CustomerMessages.WITHDRAWAL_SUCCESSFUL)
    details_page.go_to_transactions(expected_count=3)
    details_page.expect_transaction_row_contains(balance=50, transaction_type="Debit")
    details_page.back_to_account_summary()
    details_page.expect_account_details(balance=50, currency=currency)

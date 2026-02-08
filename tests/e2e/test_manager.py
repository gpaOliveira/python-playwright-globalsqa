from faker import Faker
from pages.base.Currency import Currency
from pages.customer.DetailsCustomer import CustomerMessages
from pages.customer.LoginCustomer import LoginCustomer
from pages.manager.LoginManager import LoginManager


def test_manager_create_customer(
    login_manager: LoginManager, faker: Faker, login_customer: LoginCustomer
):
    """Manager can create a customer (without an account)"""
    first_name = faker.first_name()
    last_name = faker.last_name()

    # Create our customer
    add_customer_page = login_manager.navigate_to_add_customer()
    add_customer_page.add_customer(
        first_name=first_name, last_name=last_name, post_code=faker.postcode()
    )

    # Check we can login with the newly created customer, even when they have no account
    login_customer.navigate()
    details_page = login_customer.login(label=f"{first_name} {last_name}")
    details_page.expect_message(CustomerMessages.NO_ACCOUNT)


def test_manager_create_customer_with_account(
    login_manager: LoginManager, faker: Faker, login_customer: LoginCustomer
):
    """Manager can create a customer with an account (with Dollar) but not withdraw money since they have no balance"""
    first_name = faker.first_name()
    last_name = faker.last_name()
    currency = Currency.DOLLAR

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

    # Check customer cannot withdraw money from their account since they have no money in it
    details_page.withdraw(amount=10)
    details_page.expect_message(CustomerMessages.WITHDRAWAL_ERROR)


def test_manager_create_customer_then_delete(
    login_manager: LoginManager, faker: Faker, login_customer: LoginCustomer
):
    """Manager can create a customer and then delete it"""
    first_name = faker.first_name()
    last_name = faker.last_name()
    post_code = faker.postcode()

    # Create our customer
    add_customer_page = login_manager.navigate_to_add_customer()
    add_customer_page.add_customer(
        first_name=first_name, last_name=last_name, post_code=post_code
    )

    # Search then delete our customer
    list_customers_page = login_manager.navigate_to_list_customers()
    list_customers_page.search(last_name)
    list_customers_page.expect_row_data(
        first_name=first_name, last_name=last_name, post_code=post_code
    )
    list_customers_page.delete_row_index(0)

    # Check we do not see our customer listed to login
    login_manager.home_button.click()
    login_customer.navigate_login_customer()
    logins = login_customer.get_available_customers_to_login()
    assert f"{first_name} {last_name}" not in logins

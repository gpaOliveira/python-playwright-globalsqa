from faker import Faker
from pages.CreateNewCustomer import CreateNewCustomer
from pages.LoginCustomer import LoginCustomer


def test_manager_create_customer(
    create_customer: CreateNewCustomer, faker: Faker, login_customer: LoginCustomer
):
    """Manager can create a customer (without an account)"""
    first_name = faker.first_name()
    last_name = faker.last_name()

    # Create our customer
    create_customer.navigate()
    create_customer.add_customer(
        first_name=first_name, last_name=last_name, post_code=faker.postcode()
    )

    # Check we can login with the newly created customer, even when they have no account
    login_customer.navigate()
    login_customer.login(label=f"{first_name} {last_name}")
    login_customer.expect_no_account_message()

from pages.LoginCustomer import LoginCustomer


def test_login_as_customer(login_customer: LoginCustomer):
    """First customer can login"""
    login_customer.navigate()
    login_customer.login(index=0)


def test_logout_as_customer(login_customer: LoginCustomer):
    """First customer can logout and see the list of customers to login again"""
    login_customer.navigate()
    details_page = login_customer.login(index=0)
    details_page.logout()
    assert [] != login_customer.get_available_customers_to_login()

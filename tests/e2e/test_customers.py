from pages.LoginCustomer import LoginCustomer


def test_login_as_customer(login_customer: LoginCustomer):
    """First customer can login"""
    login_customer.navigate()
    login_customer.login(index=0)

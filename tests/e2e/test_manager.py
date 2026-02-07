from pages.LoginManager import LoginManager


def test_manager_create_customer(login_manager: LoginManager):
    """Manager customer can create a customer (without an account)"""
    login_manager.navigate()

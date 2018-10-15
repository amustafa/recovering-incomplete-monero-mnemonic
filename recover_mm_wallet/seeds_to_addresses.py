"""
MyMonero.com Seeds to Addresses

This is the script to convert the discovered seeds into actual addresses and
    keys that are using to view account information for mymonero.com

This loads mymonero.com using selenium and calls the function needed to get
    account info.
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def load_driver():
    """
    Loads the firefox driver in headless mode.
    """
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    return driver


def load_my_monero(driver=None):
    """
    Will load a driver if none is passed and sets the
    url to mymonero.com
    """
    if driver is None:
        driver = load_driver()

    if "mymonero" not in driver.current_url:
        driver.get('http://mymonero.com/')

    return driver


def create_address_from_seed(seed, driver=None):
    """
    Calls the javascript function to convert a seed into an address
    and returns the information.
    """
    driver = load_my_monero(driver)
    cmd = f"return cnUtil.create_address('{seed}')"
    return driver.execute_script(cmd)


def convert_seeds_to_addresses(seeds, driver=None):
    """
    Takes a list of seeds and returns a list of dictionaries with account
        details.
    """
    driver = load_my_monero(driver)
    addresses = []
    for seed in seeds:
        addresses.append(create_address_from_seed(seed, driver))
    return addresses


def add_addresses_from_seeds(accounts_info, driver=None):
    """
    Takes a list of dictionaries that include an address seed and updates
    the dict with account info.
    """
    driver = load_my_monero(driver)
    for account_info in accounts_info:
        seed = account_info['seed']
        account_info.update(create_address_from_seed(seed, driver))

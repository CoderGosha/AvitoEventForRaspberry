'''
    Метод проксирует запросы на нужного провайдера
'''
import json
import logging
import os
from sys import path

from selenium.webdriver.webkitgtk.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from configuration import Configuration
from selenium import webdriver

def _chrome_options_():

    # proxy = configuration.config['PROXY']

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('enable-automation')
    options.add_argument('disable-infobars')
    options.add_argument('disable-gpu')
    options.add_argument('disable-browser-side-navigation')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('log-level=3')
    options.add_argument("--disable-javascript")
    # if proxy:
    #    pass
    #    options.add_argument('--proxy-server=socks5://' + proxy)
    return options


def _firefox_options_():
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument('--headless')
    return options


class RequestService:
    #     driver = webdriver.Chrome(ChromeDriverManager().install(), options=_chrome_options_())
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=_firefox_options_())
    init_browser = False
    init_provider = False

    def __init__(self):
        self.configuration = Configuration()
        self.provider = self.configuration.config['PROVIDER']['TYPE']

    def __init_browser__(self):
        configuration = Configuration()
        import logging
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.INFO)
        self.driver.set_page_load_timeout(300)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(10)

        # self.proxy = configuration.config['PROXY']
    def __init_provider__(self):
        if self.provider == "LOCAL":
            pass

    def get(self, url) -> WebDriver:
        if not self.init_browser:
            self.__init_browser__()

        if not self.init_provider:
            self.__init_provider__()

        if self.provider == "LOCAL":
            self.driver.get(url)
        else:
            logging.error(f"Unknown provider: {self.provider}")
            os._exit(1)

        return self.driver


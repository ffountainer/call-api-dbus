from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By


appium_server_url = f'http://localhost:4723'
appium_server_capabilities = {
    'automationName': 'Aurora',
    'platformName': 'Aurora',
    'platformVersion': '5.1.5.105',
    'newCommandTimeout': 86400,
    'appPackage': 'ru/auroraos/demos/CallApiDBus',
    'deviceName': '192.168.2.15',
    'autoLaunch': False,
    'appiumInspector': False,
}

def create_driver():
    appium_driver_options = AppiumOptions().load_capabilities(appium_server_capabilities)
    driver = webdriver.Remote(appium_server_url, options=appium_driver_options)
    return driver


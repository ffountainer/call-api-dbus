from helpers import driver_init, compare_images
from selenium.webdriver.common import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestOutgoingCall50556:

    def setup_method(self):
        self.driver = driver_init.create_driver()
        # create an appium driver for the tests :0

    def test(self):

        driver = self.driver

        # step 1

        driver.activate_app("ru/auroraos/demos/CallApiDBus")

        # 1.1 check if there is a loading screen

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "defaultCover"))
        )
        
        state = driver.query_app_state("ru/auroraos/demos/CallApiDBus")
        assert state == "RUNNING_IN_FOREGROUND"

        covers = driver.find_elements(By.ID, "defaultCover")
        if covers:
            assert covers[0].is_displayed()

        # 1.2 compare screenshots

        driver.screenshot("./../screenshots/actual/load.png")

        # initially I wanted to try and compare screenshots directly
        # but understood that it was a bad idea
        # since the test cases file does not contain many of them

        # assert compare_images(
        #     "./../screenshots/expected/load.png", "./../screenshots/actual/load.png"
        # )

        # 1.3 check if the main page has opened

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mainPage"))
        )

        main_page = driver.find_element(By.ID, "mainPage")
        assert main_page.is_displayed()

        # 1.4 compare screens

        driver.screenshot("./../screenshots/actual/main.png")

        # step 2

        # 2.1 start outgoig call
        button = driver.find_element(By.ID, "outgoingCallButton")
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        contact = driver.find_element(By.XPATH, "//*[contains(@text, 'Remote name')]")
        assert contact.is_displayed()

        connection = driver.find_element(By.XPATH, "//*[contains(@text, 'Соединение')]")
        assert connection.is_displayed()

        # 2.2 compare screens

        driver.screenshot("./../screenshots/actual/connection.png")

        # check for started timer
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@text, ':')]"))
        )

        # 2.3 call answered

        driver.screenshot("./../screenshots/actual/call_page.png")

        # step 3

        ## since it is on the system window, I don't have access to the correct name of the element
        end_button = driver.find_element(By.ID, "endCallButton")
        end_button.click()

        # 3.1 call ends

        # 3.2 return to main

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "mainPage"))
        )

        main_page_end = driver.find_element(By.ID, "mainPage")
        assert main_page_end.is_displayed()

        # 3.3

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Вызов завершён')]")
            )
        )

        window_id = driver.execute_script(
            "appium:findWindowByElement",
            {"strategy": By.XPATH, "value": "//*[contains(@text, 'Вызов завершён')]"},
        )

        driver.execute_script("appium:setWindow", {"windowId": window_id})

        ended = driver.find_element(By.XPATH, "//*[contains(@text, 'Вызов завершён')]")
        assert ended.is_displayed()

        time = driver.find_element(By.XPATH, "//*[contains(@text, ':')]")
        assert time.is_displayed()

        # 3.4

        driver.screenshot("./../screenshots/actual/call_ended.png")

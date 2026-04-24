from helpers import driver_init, compare_images
from selenium.webdriver.common import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import time


class TestIncomingCall50557:
    def setup_method(self):
        self.driver = driver_init.create_driver()
        # create an appium driver for the tests :0

    def test(self):

        driver = self.driver

        # step 1 (click on the icon)

        driver.activate_app("ru/auroraos/demos/CallApiDBus")

        # I do not have access to the system elements,
        # but I could have used this If I did
        driver.find_element(By.ID, "CallApiDBus").click()

        # 1.1 the main page is displayed

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mainPage"))
        )

        main_page = driver.find_element(By.ID, "mainPage")
        assert main_page.is_displayed()

        # 1.2

        calls = driver.find_element(
            By.XPATH,
            "//SectionHeader[contains(@text, 'Call') or contains(@text, 'Звонки')]",
        )

        assert calls.is_displayed()

        incoming = driver.find_element(By.ID, "incomingCallButton")

        assert incoming.is_displayed()

        inc_text = incoming.get_attribute("text")
        assert inc_text in ["Incoming call", "Входящий вызов"]

        outgoing = driver.find_element(By.ID, "outgoingCallButton")

        assert outgoing.is_displayed()

        out_text = outgoing.get_attribute("text")

        assert out_text in ["Outgoing call", "Исходящий вызов"]

        # 1.3

        functions = driver.find_element(
            By.XPATH,
            "//SectionHeader[contains(@text, 'Functions') or contains(@text, 'Функции')]",
        )

        assert functions.is_displayed()

        hold_switch = driver.find_element(
            By.XPATH,
            "//TextSwitch[contains(@text, 'Hold') or contains(@text, 'Удержание')]"
        )

        assert hold_switch.is_displayed()
        assert not hold_switch.is_selected()

        dtmf_switch = driver.find_element(
            By.XPATH,
            "//TextSwitch[contains(@text, 'DTMF')]"
        )

        assert dtmf_switch.is_displayed()
        assert not dtmf_switch.is_selected()

        # 1.4

        driver.screenshot("./../screenshots/actual/main_no_options.png")

        # step 2 (click on incoming button)

        incoming.click()

        # 2.1

        left = set()
        numbers = []

        start_time = time.time()

        assert not incoming.is_selected() and not outgoing.is_selected()
        assert not hold_switch.is_selected() and not dtmf_switch.is_selected()

        while time.time() - start_time < 6:
            text = driver.find_element(By.ID, "incomingCallButton").text

            match = re.search(r"\((\d+)\)", text)
            if match:
                val = int(match.group(1))
                left.add(val)
                numbers.append(val)

            time.sleep(0.2)

        # here I check that the timer was actually updating
        assert len(left) >= 5

        # 2.2 and 2.3

        # checked in previous step while checking timer

        # 2.4

        driver.screenshot("./../screenshots/actual/timer.png")

        # 2.5

        contact = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        assert contact.is_displayed()

        # 2.6 I cannot check vibration state here 

        # 2.7

        driver.screenshot("./../screenshots/actual/start_incoming.png")

        # step 3

        contact.find_element(By.XPATH, ".//Button").click()











        


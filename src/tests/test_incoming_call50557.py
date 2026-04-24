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
        # driver.find_element(By.ID, "CallApiDBus").click()

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
            "//TextSwitch[contains(@text, 'Hold') or contains(@text, 'Удержание')]",
        )

        assert hold_switch.is_displayed()
        assert not hold_switch.is_selected()

        dtmf_switch = driver.find_element(
            By.XPATH, "//TextSwitch[contains(@text, 'DTMF')]"
        )

        assert dtmf_switch.is_displayed()
        assert not dtmf_switch.is_selected()

        # 1.4

        driver.screenshot("./../screenshots/actual/50557/main_no_options.png")

        # step 2 (click on incoming button)

        incoming.click()

        # 2.1

        def get_timer_value():
            text = driver.find_element(By.ID, "incomingCallButton").text
            match = re.search(r"\((\d+)\)", text)
            return int(match.group(1)) if match else None

        # can we see 5 seconds left?
        WebDriverWait(driver, 5).until(lambda d: get_timer_value() == 5)

        assert not incoming.is_enabled()
        assert not outgoing.is_enabled()
        assert not hold_switch.is_enabled()
        assert not dtmf_switch.is_enabled()

        # can we see 0?
        WebDriverWait(driver, 7).until(lambda d: get_timer_value() in (0, None))

        # 2.2 and 2.3

        # checked in previous step while checking timer

        # 2.4

        driver.screenshot("./../screenshots/actual/50557/timer.png")

        # 2.5

        contact = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        assert contact.is_displayed()

        # 2.6 I cannot check vibration state here

        # 2.7

        driver.screenshot("./../screenshots/actual/50557/start_incoming.png")

        # step 3

        green = driver.find_element(By.XPATH, "//*[contains(@text, 'Принять')]")

        green.click()

        # 3.1

        driver.execute_script("app:waitForPageChange", 3000)

        # 3.2 cannot check vibro

        # 3.3 cannot check music

        # 3.4

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 3.5

        speaker = driver.find_element(By.XPATH, "//*[contains(@text, 'Динамик')]")
        volume_off = driver.find_element(By.XPATH, "//*[contains(@text, 'Откл. звук')]")
        dbus_api = driver.find_element(
            By.XPATH, "//*[contains(@text, 'Call API DBus')]"
        )

        assert speaker.is_displayed() and speaker.is_enabled()
        assert volume_off.is_displayed() and volume_off.is_enabled()
        assert dbus_api.is_displayed() and dbus_api.is_enabled()

        # 3.6

        keyboard = driver.find_element(By.XPATH, "//*[contains(@text, 'Клавиатура')]")
        record = driver.find_element(By.XPATH, "//*[contains(@text, 'Запись')]")
        hold = driver.find_element(By.XPATH, "//*[contains(@text, 'Удержание')]")

        assert keyboard.is_displayed() and not keyboard.is_enabled()
        assert record.is_displayed() and not record.is_enabled()
        assert hold.is_displayed() and not hold.is_enabled()

        # 3.7

        driver.screenshot("./../screenshots/actual/50557/call_in_process.png")

        # step 4

        # thats a system window and doesn't expose any text, so I cannot find it reliably...
        buttons = driver.find_elements(By.CLASS_NAME, "Button")
        buttons[-1].click()

        # 4.1 call ended

        driver.execute_script("app:waitForPageChange", 3000)

        # 4.2

        history = driver.find_element(By.XPATH, "//*[contains(@text, 'История')]")
        assert history.is_displayed()

        # 4.3

        window_id = driver.execute_script(
            "appium:findWindowByElement",
            {"strategy": By.XPATH, "value": "//*[contains(@text, 'Вызов завершён')]"},
        )

        driver.execute_script("appium:setWindow", {"windowId": window_id})

        ended = driver.find_element(By.XPATH, "//*[contains(@text, 'Вызов завершён')]")
        assert ended.is_displayed()

        time_element = driver.find_element(
            By.XPATH, "//*[contains(@text, ':') and contains(@text, '0')]"
        )

        time_text = time_element.text

        assert re.match(r"^\d{2}:\d{2}:\d{2}$", time_text)

        # 4.4

        driver.screenshot("./../screenshots/actual/50557/call_ended.png")

        # step 5

        button_close = driver.find_element(By.CLASS_NAME, "Button")
        button_close.click()

        # 5.1

        elements = driver.find_elements(
            By.XPATH, "//*[contains(@text, 'Вызов завершён')]"
        )
        assert len(elements) == 0

        # 5.2

        driver.screenshot("./../screenshots/actual/50557/close_pop_up.png")

        # step 6

        driver.execute_script("app:swipe", "up")

        # 6.1 && 6.2

        driver.screenshot("./../screenshots/actual/50557/home.png")

        # step 7

        widget = driver.find_element(By.XPATH, "//*[contains(@text, 'Call API DBus')]")
        widget.click()

        # 7.1

        state = driver.query_app_state("ru.auroraos.demos/CallApiDBus")
        assert state == "RUNNING_IN_FOREGROUND"

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "mainPage"))
        )

        main_page = driver.find_element(By.ID, "mainPage")
        assert main_page.is_displayed()

        # 7.2

        driver.screenshot("./../screenshots/actual/50557/return_to_main.png")

        # step 8

        incoming.click()

        # 8.1

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

        # 8.2 and 8.3

        # checked in previous step while checking timer

        # 8.4

        driver.screenshot("./../screenshots/actual/50557/timer.png")

        # 8.5

        contact = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        assert contact.is_displayed()

        # 8.6 I cannot check vibration state here

        # 8.7

        driver.screenshot("./../screenshots/actual/50557/start_incoming.png")

        # step 9

        red = driver.find_element(By.XPATH, "//*[contains(@text, 'Отклонить')]")

        red.click()

        # 9.1

        driver.execute_script("app:waitForPageChange", 3000)

        # 9.2

        window_id = driver.execute_script(
            "appium:findWindowByElement",
            {"strategy": By.XPATH, "value": "//*[contains(@text, 'Вызов завершён')]"},
        )

        driver.execute_script("appium:setWindow", {"windowId": window_id})

        ended = driver.find_element(By.XPATH, "//*[contains(@text, 'Вызов завершён')]")
        assert ended.is_displayed()

        remote = driver.find_element(By.XPATH, "//*[contains(@text, 'Remote name')]")

        assert remote.is_displayed()

        time_element = driver.find_element(
            By.XPATH, "//*[contains(@text, ':') and contains(@text, '0')]"
        )

        time_text = time_element.text

        assert re.match(r"^\d{2}:\d{2}:\d{2}$", time_text)

        assert time_text == "00:00:00"

        # 9.3

        driver.screenshot("./../screenshots/actual/50557/call_ended_right_away.png")

        # step 10

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

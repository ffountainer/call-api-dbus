from helpers import driver_init, compare_images
from selenium.webdriver.common import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


class TestIncomingKeyboard53610:
    def setup_method(self):
        self.driver = driver_init.create_driver()
        # create an appium driver for the tests :0

    def test(self):

        driver = self.driver

        # step 1 (activate app)

        driver.activate_app("ru/auroraos/demos/CallApiDBus")

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

        driver.screenshot("./../screenshots/actual/53610/main_no_options.png")

        # step 2

        dtmf_switch.click()

        # 2.1

        assert dtmf_switch.is_selected()

        # 2.2

        label = driver.find_element(By.XPATH, "//*[contains(@text, 'Текст DTMF')]")
        assert label.is_displayed()

        # 2.3

        driver.screenshot("./../screenshots/actual/53610/keyboard_on.png")

        # step 3

        incoming.click()

        # 3.1

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

        # 3.2 and 3.3

        # checked in previous step while checking timer

        # 3.4

        driver.screenshot("./../screenshots/actual/53610/timer.png")

        # 3.5

        contact = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        assert contact.is_displayed()

        # 3.6 I cannot check vibration state here

        # 3.7

        driver.screenshot("./../screenshots/actual/53610/start_incoming.png")

        # step 4

        green = driver.find_element(By.XPATH, "//*[contains(@text, 'Принять')]")

        green.click()

        # 4.1

        driver.execute_script("app:waitForPageChange", 3000)

        # 4.2 cannot check vibro

        # 4.3 cannot check music

        # 4.4

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 4.5

        speaker = driver.find_element(By.XPATH, "//*[contains(@text, 'Динамик')]")
        volume_off = driver.find_element(By.XPATH, "//*[contains(@text, 'Откл. звук')]")
        dbus_api = driver.find_element(
            By.XPATH, "//*[contains(@text, 'Call API DBus')]"
        )
        keyboard = driver.find_element(By.XPATH, "//*[contains(@text, 'Клавиатура')]")
        
        assert speaker.is_displayed() and speaker.is_enabled()
        assert volume_off.is_displayed() and volume_off.is_enabled()
        assert dbus_api.is_displayed() and dbus_api.is_enabled()
        assert keyboard.is_displayed() and keyboard.is_enabled()

        # 4.6

        hold = driver.find_element(By.XPATH, "//*[contains(@text, 'Удержание')]")
        record = driver.find_element(By.XPATH, "//*[contains(@text, 'Запись')]")
        
        assert record.is_displayed() and not record.is_enabled()
        assert hold.is_displayed() and not hold.is_enabled()

        # 4.7

        driver.screenshot("./../screenshots/actual/53610/call_in_process.png")

        # step 5

        keyboard.click()

        # 5.1

        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 5.2

        assert not speaker.is_displayed() 
        assert not volume_off.is_displayed() 
        assert not dbus_api.is_displayed() 
        assert not keyboard.is_displayed()
        assert not record.is_displayed()
        assert not hold.is_displayed()

        # 5.3

        assert driver.is_keyboard_shown()

        # 5.4

        hide_button = driver.find_element(By.XPATH, "//*[contains(@text, 'Скрыть')]")

        assert hide_button.is_displayed()

        # 5.5

        driver.screenshot("./../screenshots/actual/53610/keyboard_opened.png")

        # step 6

        driver.execute_script('app:enterCode', '*102#')

        # 6.1

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, '*102#')]")
            )
        )

        # 6.2

        driver.screenshot("./../screenshots/actual/53610/entered_code.png")

        # step 7

        hide_button.click()

        # 7.1

        assert not driver.is_keyboard_shown()

        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(@text, '*102#')]")
            )
        )

        # 7.2

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 7.3

        assert speaker.is_displayed() and speaker.is_enabled()
        assert volume_off.is_displayed() and volume_off.is_enabled()
        assert dbus_api.is_displayed() and dbus_api.is_enabled()
        assert keyboard.is_displayed() and keyboard.is_enabled()

        # 7.4

        assert record.is_displayed() and not record.is_enabled()
        assert hold.is_displayed() and not hold.is_enabled()

        # 7.5

        driver.screenshot("./../screenshots/actual/53610/keyboard_hidden.png")

        # step 8

        # thats a system window and doesn't expose any text, so I cannot find it reliably...
        buttons = driver.find_elements(By.CLASS_NAME, "Button")
        buttons[-1].click()

        # 8.1 call ended

        driver.execute_script("app:waitForPageChange", 3000)

        history = driver.find_element(By.XPATH, "//*[contains(@text, 'История')]")
        assert history.is_displayed()

        # 8.2

        window_id = driver.execute_script(
            "appium:findWindowByElement",
            {"strategy": By.XPATH, "value": "//*[contains(@text, 'Вызов завершен')]"},
        )

        driver.execute_script("appium:setWindow", {"windowId": window_id})

        ended = driver.find_element(By.XPATH, "//*[contains(@text, 'Вызов завершен')]")
        assert ended.is_displayed()

        time_element = driver.find_element(
            By.XPATH, "//*[contains(@text, ':') and contains(@text, '0')]"
        )

        time_text = time_element.text

        assert re.match(r"^\d{2}:\d{2}:\d{2}$", time_text)

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 8.3

        driver.screenshot("./../screenshots/actual/53610/call_ended.png")

        # step 9

        button_close = driver.find_element(By.CLASS_NAME, "Button")
        button_close.click()

        # 9.1

        elements = driver.find_elements(
            By.XPATH, "//*[contains(@text, 'Вызов завершен')]"
        )
        assert len(elements) == 0

        # 9.2

        driver.screenshot("./../screenshots/actual/53610/close_pop_up.png")

        # step 10

        driver.execute_script("app:swipe", "up")

        # 10.1 && 10.2

        driver.screenshot("./../screenshots/actual/53610/home.png")

        # step 11

        widget = driver.find_element(By.XPATH, "//*[contains(@text, 'Call API DBus')]")
        widget.click()

        # 11.1

        state = driver.query_app_state("ru.auroraos.demos/CallApiDBus")
        assert state == "RUNNING_IN_FOREGROUND"

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "mainPage"))
        )

        main_page = driver.find_element(By.ID, "mainPage")
        assert main_page.is_displayed()

        # 11.2

        keyboard_second = driver.find_element(By.XPATH, "//*[contains(@text, 'DTMF')]")
        assert keyboard_second.is_selected()

        # 11.3

        label = driver.find_element(By.XPATH, "//TextArea")
        assert label.text == "*102#"    

        # 11.4 

        driver.screenshot("./../screenshots/actual/53609/return_to_main.png")

        # step 12

        keyboard_second.click()

        # 12.1

        assert not keyboard_second.is_selected()

        # 12.2

        assert not driver.is_keyboard_shown()

        # 11.3

        driver.screenshot("./../screenshots/actual/53610/main_keyboard_off.png")




        
        



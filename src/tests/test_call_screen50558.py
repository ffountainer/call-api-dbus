from helpers import driver_init, compare_images
from selenium.webdriver.common import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestCallScreen50558:
    def setup_method(self):
        self.driver = driver_init.create_driver()
        # create an appium driver for the tests :0

    def test(self):

        driver = self.driver

        # step 1

        driver.activate_app("ru/auroraos/demos/CallApiDBus")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "incomingCallButton"))
        )

        incoming = driver.find_element(By.ID, "incomingCallButton")

        incoming.click()

        green = driver.find_element(By.XPATH, "//*[contains(@text, 'Принять')]")

        green.click()

        # 1.1

        driver.execute_script("app:waitForPageChange", 3000)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@text, 'Remote name')]")
            )
        )

        # 1.2

        driver.screenshot("./../screenshots/actual/50558/answer_incoming.png")

        # step 2

        speaker = driver.find_element(By.XPATH, "//*[contains(@text, 'Динамик')]")
        assert not speaker.is_selected()
        speaker.click()

        # 2.1

        assert speaker.is_selected()

        # 2.2

        driver.screenshot("./../screenshots/actual/50558/speaker_on.png")

        # 2.3 cannot check where the sound goes

        # step 3

        speaker.click()

        # 3.1

        assert not speaker.is_selected()

        # 3.2

        driver.screenshot("./../screenshots/actual/50558/speaker_off.png")

        # 3.3 cannot check real life speaker

        # step 4

        volume_off = driver.find_element(By.XPATH, "//*[contains(@text, 'Откл. звук')]")
        assert not volume_off.is_selected()
        volume_off.click()

        # 4.1

        assert volume_off.is_selected()

        # 4.2

        driver.screenshot("./../screenshots/actual/50558/volume_off.png")

        # 4.3 cannot check if the mic is off

        # step 5

        volume_off.click()

        # 5.1

        assert not volume_off.is_selected()

        # 5.2

        driver.screenshot("./../screenshots/actual/50558/volume_on.png")

        # 5.3 cannot checl real mic

        # step 6

        keyboard = driver.find_element(By.XPATH, "//*[contains(@text, 'Клавиатура')]")
        assert not keyboard.is_selected()
        keyboard.click()

        # 6.1 & 6.2

        assert not keyboard.is_enabled()

        # step 7

        hold = driver.find_element(By.XPATH, "//*[contains(@text, 'Удержание')]")
        assert not hold.is_selected()
        hold.click()

        # 7.1 & 7.2

        assert not hold.is_enabled()

        # step 8

        record = driver.find_element(By.XPATH, "//*[contains(@text, 'Запись')]")
        assert not record.is_selected()
        record.click()

        # 8.1 & 8.2

        assert not record.is_enabled()

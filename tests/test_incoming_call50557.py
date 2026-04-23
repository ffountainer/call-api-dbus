from helpers import driver_init, compare_images
from selenium.webdriver.common import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestIncomingCall50557:
    def setup_method(self):
        self.driver = driver_init.create_driver()
        # create an appium driver for the tests :0

    def test(self):

        driver = self.driver

        # step 1 (click on the icon)

        # I do not have access to the system elements, so I just supposed that the name of the element is CallApiDBus
        driver.find_element(By.ID, "CallApiDBus").click()

        # 1.1
        
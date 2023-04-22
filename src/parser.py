from typing import List, Dict, Any, Optional
import pyperclip
import time

from selenium.webdriver import ChromeOptions, ActionChains, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .settings import Settings
from .models import FbData, AddedApps

# from settings import Settings
# from models import FbData


class DriverSettings:
    """class for determining remote driver settings"""

    __SELENOID_OPTIONS = {
        "browserName": "chrome",
        "browserVersion": "96.0.46-64.45",
        "acceptSslCerts": True,
        "sessionTimeout": "876000h",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False,
            "enableLog": True,
        },
    }

    _CH_OPT = {
        "args": [
            "disable-infobars",
            "--disable-gpu",
            "no-sandbox",
            "disable-setuid-sandbox",
            "--ignore-certificate-errors",
        ],
        "w3c": False,
    }
    __IPServ = "192.168.1.113"
    __OPTIONS = ChromeOptions()
    __OPTIONS.add_argument("--headless")
    __OPTIONS.add_argument("--window-size=1920,1200")
    __OPTIONS.set_capability("browserVersion", "96.0.4664.45")
    __OPTIONS.set_capability("selenoid:options", __SELENOID_OPTIONS)
    __OPTIONS.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    __OPTIONS.set_capability("goog:chromeOptions", _CH_OPT)
    __OPTIONS.add_argument("--disable-notifications")
    __OPTIONS.add_argument("--disable-extensions")

    _DRIVER = Remote(
        command_executor=f"http://{__IPServ}:4444/wd/hub", options=__OPTIONS
    )


class BaseParser(DriverSettings): # TestDriverSettings
    """The parser to handle parsing proccess"""

    __ORIGINAL_WINDOW = None

    def login_fb(self, auth_2fa: bool = False) -> None:
        """The method which perfroms loggining fb page and puts on hold with a new tab opened"""
        driver = self._DRIVER
        self.__ORIGINAL_WINDOW = driver.current_window_handle
        driver.get(Settings.FB.Loggining.URL_LOGIN)
        time.sleep(0.5)
        pass_email = driver.find_element(By.ID, "email")
        ActionChains(driver).move_to_element(pass_email).pause(0.5).send_keys(
            Settings.FB.Loggining.LOGIN
        ).send_keys(Keys.TAB).pause(1).send_keys(
            Settings.FB.Loggining.PASSWORD
        ).send_keys(
            Keys.ENTER
        ).perform()
        time.sleep(2)
        if auth_2fa:
            driver.switch_to.new_window("tab")
            # ToDo: need to get 2fa request for code and complete a code here
            code = self.get_through_2fa()  # got code from site  # type: ignore
            driver.switch_to.window(self.__ORIGINAL_WINDOW)
        driver.switch_to.new_window("tab")

    @staticmethod
    def get_through_2fa() -> str:
        """If it needs to get through fb 2fa"""
        driver = DriverSettings._DRIVER

        driver.get(Settings.FB.Loggining.Auth2FA.URL_2FA)
        # print(Settings.FB.Loggining.Auth2FA.secret_code)
        time.sleep(1)
        driver.find_element(By.ID, "listToken").send_keys(
            Settings.FB.Loggining.Auth2FA.SECRET_CODE
        )
        time.sleep(0.5)
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        driver.find_element(By.ID, "copy_btn").click()
        return pyperclip.paste()

    def get_all_apps(self) -> Dict[str, List[Optional[int]]]:
        """method to get the whole list of app`s ids

        Args:
            app_id (int, optional): the set of numbers means unique id of fb application.

        Returns:
            List[str]: list with the whole available applications in your business acc
        """
        driver = self._DRIVER
        driver.get(Settings.FB.URL_APPS)
        time.sleep(2)
        apps_divs = driver.find_elements(
            By.CLASS_NAME, Settings.FB.TagsAtribsParams.Params.APP_CLASS
        )
        apps_id = [
            span.find_element(By.TAG_NAME, "span").text.split(":")[1].strip()
            for span in apps_divs
        ]
        time.sleep(2)
        return FbData(app_id=apps_id)  # type: ignore

    def find_adv_apps_pallete(self, app_id: Optional[int]) -> Any:
        """method for run seeking out advertisement ids in fb settings advertising apps

        Args:
            app_id (int, optional): the set of numbers means unique id of fb application.

        Returns:
            Union[None, Any]: either None nor returns html element for further using
        """
        driver = self._DRIVER
        driver.get(Settings.FB.URL_ADV_APPS.format(app_id))
        time.sleep(2)
        adv_pallete = driver.find_element(
            By.XPATH, Settings.FB.TagsAtribsParams.XPath.ADS_PALLETTE
        )
        ActionChains(driver).scroll_to_element(adv_pallete).perform()

        return adv_pallete

    def get_adv_apps(self, app_id: Optional[int]) -> FbData:
        """method for run getting out advertisement ids in fb settings advertising apps

        Args:
            app_id (int, optional): the set of numbers means unique id of fb application.

        Returns:
            List[int]: list with the whole available ids wrapped in dataclass
        """
        adv_pallete = self.find_adv_apps_pallete(app_id=app_id)
        span_ids = adv_pallete.find_elements(
            By.CSS_SELECTOR, Settings.FB.TagsAtribsParams.Params.SPAN_IDS
        )
        apps_id = [int(id.text) for id in span_ids]
        time.sleep(2)
        return FbData(app_id=apps_id)

    def add_advapp_to_app(
        self, app_id: Optional[int], data: Dict[str, List[Optional[int]]]
    ) -> AddedApps:
        """method for run adding advertisement ids in fb settings advertising apps for expanding your adv profile

        Args:
            app_id (Optional[int]): the set of numbers means unique id of fb application.
            data (Dict[str, List[Optional[int]]]): being passed data

        Returns: dict with data wrapped in dataclass

        """
        driver = self._DRIVER
        adv_pallete = self.find_adv_apps_pallete(app_id=app_id)
        input_field = adv_pallete.find_element(
            By.CSS_SELECTOR, Settings.FB.TagsAtribsParams.Params.INPUT_IDS
        )
        for _id in data["accs"]:
            time.sleep(0.5)
            input_field.send_keys(_id)
            time.sleep(0.5)
            input_field.send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(
            By.XPATH, Settings.FB.TagsAtribsParams.XPath.SAVE_BUTTON
        ).click()
        time.sleep(2)
        check_apps = self.get_adv_apps(app_id=app_id)
        res = dict()
        for _id in data["accs"]:
            if _id in check_apps:
                res[_id] = True
            else:
                res[_id] = False
        return AddedApps(res)

    def remove_advapp_from_apps(
        self, app_id: Optional[int], data: Dict[str, List[Optional[int]]]
    ):
        """method for run deleting unnecessary advertisement ids in fb settings advertising apps in your adv profile

        Args:
            app_id (Optional[int]): the set of numbers means unique id of fb application
            data (Dict[str, List[Optional[int]]]): being passed data
        """
        driver = self._DRIVER
        adv_pallete = self.find_adv_apps_pallete(app_id=app_id)
        span_ids = adv_pallete.find_elements(
            By.CSS_SELECTOR, Settings.FB.TagsAtribsParams.Params.SPAN_IDS
        )
        for _id in data["accs"]:  # ids deletes but not saves. tests failed!
            for span in span_ids:
                if _id == int(span.text):
                    trg = span.find_element(By.XPATH, "span/div/div[2]/span")
                    time.sleep(0.5)
                    trg.click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, Settings.FB.TagsAtribsParams.XPath.SAVE_BUTTON
        ).click()
        time.sleep(2)

    def shut_down_the_driver(self):
        """Abborting and exiting the current being runned driver"""
        self._DRIVER.close()
        self._DRIVER.quit()

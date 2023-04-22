from selenium.webdriver import  ChromeOptions, Chrome
from ..parser import BaseParser



class TestDriverSettings:

    __OPTIONS = ChromeOptions()
    __OPTIONS.add_argument("--window-size=1920,1200")
    _DRIVER = Chrome(options=__OPTIONS)


if __name__ == "__main__":

    # Checking the act of selenium driver without using fast_api and outer api
    
    pars = BaseParser()
    pars.login_fb()
    res = pars.add_advapp_to_app(app_id=274078654944102, data = {'accs': [466795215524374]})
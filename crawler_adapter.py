from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from common.logging import InfoLogger, ErrorLogger

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

class CrawlerAdapter:
    def __init__(self):
        self.driver = None
        self.action = None

    def init(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.action = ActionChains(self.driver)
            self.driver.set_window_size(1920, 1080)
        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.init.init_driver_and_action_fail. {str({"error": e})}')
            return e

        return None

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            ErrorLogger.error('crawler_adapter.close.close_driver_fail')
            return e

        return None

    def get(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get.driver_get_url_fail. Details {str({"error": e})}')
            return e

        return None

    def get_element_by_xpath(self, xpath, timeout=None):
        if timeout:
            try:
                _ = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException as e:
                ErrorLogger.error(f'crawler_adapter.get_element_by_xpath.timeout. Details: {str({"xpath": xpath})}')
                return None, e
            except Exception as e:
                ErrorLogger.error(f'crawler_adapter.get_element_by_xpath.unknown_error. Details: {str({"xpath": xpath, "error": e})}')
                return None, e

        try:
            elem = self.driver.find_element(By.XPATH, xpath)
        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_element_by_xpath.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return elem, None

    def get_elements_by_xpath(self, xpath, timeout=None):
        if timeout:
            try:
                _ = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException as e:
                ErrorLogger.error(f'crawler_adapter.get_elements_by_xpath.timeout. Details: {str({"xpath": xpath})}')
                return None, e
            except Exception as e:
                ErrorLogger.error(f'crawler_adapter.get_elements_by_xpath.unknown_error. Details: {str({"xpath": xpath, "error": e})}')
                return None, e

        try:
            elem = self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_element_by_xpath.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return elem, None

    def click(self, xpath, offset=None, timeout=None):
        try:
            element, res = self.get_element_by_xpath(xpath, timeout)
            if res:
                ErrorLogger.error(f'crawler_adapter.click.fail.')
                return res

            self.action.move_to_element(element)
            if offset:
                self.action.move_by_offset(offset[0], offset[1])
            sleep(3)

            self.action.click()
            self.action.perform()

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.click.fail. Details: {str({"xpath": xpath, "error": e})}')
            return e

        return None

    def get_text(self, xpath, timeout=None):
        try:
            element, res = self.get_element_by_xpath(xpath, timeout)
            if res:
                ErrorLogger.error(f'crawler_adapter.get_text.fail.')
                return None, res

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_text.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return element.text, None

    def get_texts(self, xpath, timeout=None):
        try:
            elements, res = self.get_elements_by_xpath(xpath, timeout)
            if res:
                ErrorLogger.error(f'crawler_adapter.get_texts.fail.')
                return None, res

            elem_texts = [e.text for e in elements]

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_texts.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return elem_texts, None

    def fill_textfield(self, xpath, keys, timeout = None):
        try:
            elem, res = self.get_element_by_xpath(xpath, timeout)
            if res:
                ErrorLogger.error(f'crawler_adapter.fill_textfield.fail.')
                return res

            elem.send_keys(keys)

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.fill_textfield.fail. Details: {str({"xpath": xpath, "keys": keys, "error": e})}')
            return e

        return None

    def submit(self, xpath, timeout = None):
        try:
            elem, res = self.get_element_by_xpath(xpath, timeout)
            if res:
                ErrorLogger.error(f'crawler_adapter.submit.fail.')
                return res

            elem.submit()

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.submit.fail. Details: {str({"xpath": xpath, "error": e})}')
            return e

        return None

    def get_attribute(self, xpath, attr):
        try:
            elem, res = self.get_element_by_xpath(xpath)
            if res:
                ErrorLogger.error(f'crawler_adapter.get_attribute.fail.')
                return res

            attr_value = elem.get_attribute(attr)

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_attribute.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return attr_value, None

    def get_attributes(self, xpath, attr):
        try:
            elems, res = self.get_elements_by_xpath(xpath)
            if res: return res

            attr_values = [elem.get_attribute(attr) for elem in elems]

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.get_attributes.fail. Details: {str({"xpath": xpath, "error": e})}')
            return None, e

        return attr_values, None

    def screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.screenshot.fail. Details: {str({"filename": filename, "error": e})}')
            return e

        return None

    def type(self, keys):
        try:
            self.action.send_keys(keys).perform()

        except Exception as e:
            ErrorLogger.error(f'crawler_adapter.screenshot.fail. Details: {str({"keys": keys, "error": e})}')
            return e

        return None

from modules.proxy_plugin import proxy_plugin
from modules.files import read_executable_path_info

import json
import zipfile
import os
from sys import exit
import pickle
import time
import getpass
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# from fake_useragent import UserAgent
from multiprocessing import freeze_support
freeze_support()
import undetected_chromedriver as uc


class Scraper:

    def __init__(self, headless=False, on_failure='exit', profile='', proxy='', captcha=False):

        settings = read_executable_path_info('inputs/settings.txt', '=')
        self.browser_executable_path = settings.get('browser', None)
        self.driver_executable_path = settings.get('driver', None)
        self.chrome_version = settings.get('chrome_version', None)
        self.captcha = settings.get('captcha_extension', captcha)
        self.profile = profile
        self.headless = settings.get('headless', headless)
        self.on_failure = settings.get('on_failure', on_failure)
        self.proxy = settings.get('proxy', proxy)
        
        self.setup_driver_options(self.headless, self.proxy, self.profile, self.captcha)
        self.setup_driver()

    def __del__(self):
        pass

    # Add these options in order to make chrome driver appear as a human instead of detecting it as a bot
    def setup_driver_options(self, headless, proxy, profile, captcha):
        self.driver_options = uc.ChromeOptions()
        
        # Disable password save popup
        # prefs = {"credentials_enable_service": False,
        #          "profile.password_manager_enabled": False}
        # self.driver_options.add_experimental_option("prefs", prefs)

        arguments = [
            # f'--user-agent={user_agent}',
            # '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36',
            # '--start-maximized',
            # '--disable-blink-features=AutomationControlled',              # This will solve the driver.get(url) error & also selenium detection, chrome shows warning
            # '--disable-dev-shm-usage',                                    # May be required for headless chrome
            # '--no-sandbox',                                               # with sandbox, one tab cannot watch another tab
            # '--disable-popup-blocking',                                     # Otherwise new tab will not be opened
            '--no-first-run --no-service-autorun --password-store=basic',   # just some options passing in to skip annoying popups
        ]
        # self.driver_options.add_argument("window-size=1400,600")
        if profile:
            arguments.append(f'--user-data-dir=c:\\temp\\{profile}')     # Saving user profile, It causes the error sometimes like 127.0.0 chrome not found

        for argument in arguments:
            self.driver_options.add_argument(argument)
            

        if headless:
            self.driver_options.add_argument('--headless')

        # self.driver_options.add_argument('--proxy-server=223.96.90.216:8085')
        if proxy:
            pluginfolder = proxy_plugin(proxy)
            pluginfolder = os.path.join(os.getcwd(), pluginfolder)
        if captcha:
            capcha_path = os.path.join(os.getcwd(), 'captcha')
            
        if proxy and captcha:
            self.driver_options.add_argument(f'--load-extension={capcha_path},{pluginfolder}')
        elif proxy:
            self.driver_options.add_argument(f'--load-extension={pluginfolder}')
        elif captcha:
            self.driver_options.add_argument(f'--load-extension={capcha_path}')

    # Setup chrome driver with predefined options
    def setup_driver(self):
        # self.print_executable_path()
        self.driver = uc.Chrome(
            options=self.driver_options,
            driver_executable_path=self.driver_executable_path,
            browser_executable_path=self.browser_executable_path,
            version_main=self.chrome_version,
            # use_subprocess = True,
        )
        # self.s = Service(executable_path=self.driver_executable_path)
        # self.driver = webdriver.Chrome(service=self.s, options = self.driver_options)

    def print_executable_path(self):
        print('chrome browser path:', self.browser_executable_path)
        print('chromedriver path:', self.driver_executable_path)
        print('chrome version:', self.chrome_version)
        print('Exit:', self.on_failure)
        print('headless:', self.headless)
        print('proxy:', self.proxy)
        
    # Add login functionality and load cookies if there are any with 'cookies_file_name'
    def add_login_functionality(self, is_logged_in_selector, login_function=None, exit_on_login_failure=True, cookies_file_name='cookies'):
        # Three step Login. 1:Using cookies, 2:By Selenium UI automation, 3:Manual login Then press any key
        self.is_logged_in_selector = is_logged_in_selector
        self.cookies_folder = 'cookies' + os.path.sep
        self.cookies_file_path = self.cookies_folder + cookies_file_name + '.pkl'
        self.login_status = self.is_logged_in()

        # Step 1: Check if there is a cookie file saved
        if self.login_status == False:
            if os.path.exists(self.cookies_file_path):
                self.load_cookies()
                # Check if user is logged in after adding the cookies
                self.login_status = self.is_logged_in()

        # Step 2: Call the login method for Selenium UI interaction login
        if self.login_status == False:
            if login_function:
                login_function()
                self.login_status = self.is_logged_in()  # Check if user is logged in

        # Step 3: Manual Login
        if self.login_status == False:
            input('Login manually, Then press ENTER...')
            self.sleep(1.0, 3.0)
            self.login_status = self.is_logged_in()  # Check if user is logged in

        if self.login_status == True:
            self.save_cookies()		# User is logged in. So, save the cookies
        elif exit_on_login_failure == True:
            self.handle_exception('Sorry, We are failed to be logged In.', on_failure='exit')

        return self.login_status

    # Load cookies from file
    def load_cookies(self):
        # Load cookies from the file
        cookies_file = open(self.cookies_file_path, 'rb')
        cookies = pickle.load(cookies_file)

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        cookies_file.close()
        
        print('Cookies loaded successfully')

        # self.go_to_page('url')

        # time.sleep(5)

    # Save cookies to file
    def save_cookies(self):
        # Do not save cookies if there is no cookies_file name
        if not hasattr(self, 'cookies_file_path'):
            return

        # Create folder for cookies if there is no folder in the project
        if not os.path.exists(self.cookies_folder):
            os.mkdir(self.cookies_folder)

        # Open or create cookies file
        cookies_file = open(self.cookies_file_path, 'wb')

        # Get current cookies from the driver
        cookies = self.driver.get_cookies()

        # Save cookies in the cookie file as a byte stream
        pickle.dump(cookies, cookies_file)

        cookies_file.close()

    # Check if user is logged in based on a html element that is visible only for logged in users
    def is_logged_in(self):
        element = self.find_element(self.is_logged_in_selector, on_failure='ignore', wait_element_time=3)
        return True if element else False

    # Wait random amount of seconds before taking some action so the server won't be able to tell if you are a bot
    def sleep(self, a=0.5, b=None):
        if b == None:
            random_sleep_seconds = a
        else:
            random_sleep_seconds = round(random.uniform(a, b), 2)

        time.sleep(random_sleep_seconds)

    def go_to_page(self, url):
        self.driver.get(url)

    def handle_exception(self, error, on_failure='default'):  # Utility function handles exit on missing element behavior
        if on_failure == 'default':
            on_failure = self.on_failure    # Default action (exit)
        
        if on_failure == 'exit':
            print(error)
            exit()
        elif on_failure == 'warning':
            print(error) # Warning and Ignore the error
        elif on_failure == 'pause':
            print(error)
            option = input("Program is paused,\nPress 'e' for Exception | Any key to exit | 'c' to Continue: ")
            if option == 'e':
                raise Exception(error)
            elif option == 'c':
                pass
            else:
                exit()
        elif on_failure == 'ignore':
            pass
        else:
            raise ValueError(f'on_failure type is invalid {on_failure}')

    def find_element_js(self, css_selector='', id='', class_name=''):

        if css_selector:
            element = self.driver.execute_script('return document.querySelector(arguments[0])', css_selector)
        elif id:
            element = self.driver.execute_script('return document.getElementById(arguments[0])', id)
        
        return element
    
    def find_element(self, css_selector='', xpath='', ref_element=None, wait_element_time=3, on_failure='default'):

        element = None
        driver = ref_element or self.driver

        try:
            if css_selector:
                element = WebDriverWait(driver, wait_element_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            elif xpath:
                element = WebDriverWait(driver, wait_element_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
            else:
                self.handle_exception('ERROR: CSS_SELECTOR | XPATH is required to find element', on_failure='exit')
        except TimeoutException:
            self.handle_exception(f'ERROR: Timed out waiting for the element "{css_selector or xpath}" to load', on_failure)
        except Exception as e:
            self.handle_exception(f'Unknown exception to find element "{css_selector or xpath}". Exception: {e}', on_failure)

        return element
            
    def find_elements(self, css_selector='', xpath='', ref_element=None, loop_count=1, on_failure='default'):

        elements = []
        driver = ref_element or self.driver

        i = 1
        while True:
            if css_selector:
                elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
            elif xpath:
                elements = driver.find_elements(By.XPATH, xpath)
            else:
                self.handle_exception('ERROR: CSS_SELECTOR | XPATH is required to find elements', on_failure='exit')

            if i == loop_count or elements:
                break
            else:
                i += 1
                time.sleep(1)
        
        return elements

    def click_checkbox(self, elements, index=0):
        if elements:
            self.element_click(element=elements[index])
        else:
            self.handle_exception(f'Failed to click checkbox. Elements are None.')
        
    def select_dropdown(self, element, val='', text='', delay=0.5, on_failure='default'):
        if element:
            select = Select(element)
            if delay:
                self.sleep(delay)
            
            try:
                if text:
                    select.select_by_visible_text(text)
                    return True
                elif val:
                    select.select_by_value(val)   
                    return True
                else:
                    self.handle_exception('Failed to select dropdown. Text or value must be given.', 'exit')
            except NoSuchElementException:
                self.handle_exception(f'Failed to select dropdown. No option found for {text or val}', on_failure)
        else:
            self.handle_exception(f'Failed to select dropdown. element is None.', on_failure)
        
        return False
            
    def add_emoji(self, selector, text):
        JS_ADD_TEXT_TO_INPUT = """
		var elm = arguments[0], txt = arguments[1];
		elm.value += txt;
		elm.dispatchEvent(new Event('change'));
		"""
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, element, text)
        element.send_keys('.')
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(Keys.TAB)

    def scroll(self, element=None):
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto',block: 'center',inline: 'center'});", element)
        else:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def element_click(self, element, on_failure='default', delay=0.5):
        if element:
            if delay:
                self.sleep(delay)
                
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                return self.element_click_by_js(element=element)
            except Exception as e:
                self.handle_exception(f'Unable to click element. Exception: {e}', on_failure)
        else:
            self.handle_exception(f'Unable to click element. Element is None.', on_failure)      
        return False

    # Wait random time before sending the keys to the element
    def element_send_keys(self, element, text, on_failure='default', click_input=False, clear_input=False, char_by_char=False, delay=0.5):
        if text is None:
            self.handle_exception(f'Unable to send keys. Text is None.', on_failure)
            
        if element:
            if delay:
                time.sleep(delay)
                
            try:
                if click_input:
                    self.element_click(element, on_failure='ignore', delay=None)
                if clear_input:
                    element.clear()
            
                if char_by_char:
                    text = str(text)
                    for t in text:
                        element.send_keys(t)
                        self.sleep(0.01, 0.2)
                else:
                        element.send_keys(text)
                return True
            except Exception as e:
                self.handle_exception(f'Unable to send keys. Exception: {e}', on_failure)
        else:
            self.handle_exception(f'Unable to send keys. Element is None.', on_failure)
                
        return False

    # scraper.input_file_add_files('input[accept="image/jpeg,image/png,image/webp"]', images_path)
    def input_file_add_files(self, css_selector, files, on_failure='exit'):
        input_file = self.find_element(css_selector=css_selector, on_failure=on_failure)

        self.sleep()

        try:
            input_file.send_keys(files)
        except InvalidArgumentException:
            self.handle_exception(f'ERROR: Exiting input_file_add_files! Please check if these file paths are correct:\n {files}', on_failure)

    # Wait random time before clearing the element (popup)
    def element_clear(self, element, on_failure):
        if element:              
            try:  
                element.clear()

                if element.get_attribute('value') != '':
                    element.send_keys(Keys.CONTROL + "a")
                    element.send_keys(Keys.DELETE)
                return True
            except Exception as e:
                self.handle_exception(f'Error: Unable to clear element. {e}', on_failure)
        else:        
            self.handle_exception(f'Unable to clear element. Element is None.', on_failure)
            
        return False

    def element_wait_to_be_invisible(self, selector, on_failure='default'):
        wait_until = EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))

        try:
            WebDriverWait(self.driver, self.wait_element_time).until(
                wait_until)
        except:
            self.handle_exception(f'Error: waiting the element with selector {selector} to be invisible', on_failure)

    def open_new_tab(self, url):
        self.driver.execute_script("window.open(arguments[0])", url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_tab_and_back_homepage(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_tab(self, tab_index):
        tab_index = int(tab_index)
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def element_click_by_js(self, element):
        # If the element is not clickable in normal way because element is covered by another element
        self.driver.execute_script('arguments[0].click()', element)
        return True

    def element_set_attribute(self, element, key='value', value=''):
        self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, key, value)

    def get_network_log(self):
        logs = self.driver.execute_script('''
                                    var performance = window.performance || 
                                    window.mozPerformance || 
                                    window.msPerformance || 
                                    window.webkitPerformance || {}; 
                                    var network = performance.getEntries() || {}; 
                                    return network; 
                                    ''')
        return logs

    def move_to_element(self, element):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element)
            action.perform()
            return True
        except ElementNotInteractableException:
            return False
            

    def close(self, quit=False):
        try:
            if quit:
                self.driver.quit()
            else:
                self.driver.close()
            return True
        except:
            return False

    def what_is_my_ip(self, log=True):
        ip = None
        self.open_new_tab('https://api.myip.com/')
        try:
            my_ip = self.find_element('body', wait_element_time=10).text
            my_ip = json.loads(my_ip)
            if log:
                print(f"IP: {my_ip['ip']}, Country: {my_ip['country']}")
            ip = my_ip['ip']
        except:
            print('My IP not found')
        
        self.sleep(2)
        self.close_tab_and_back_homepage()
        return ip 
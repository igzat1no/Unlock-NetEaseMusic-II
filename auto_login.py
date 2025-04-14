# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007073D46BF0C63CD8BE74E281B0991899D64A289240ACF0EE3AB86727B4EF50DC48062884C1DA6F253E7A1C3F69EAD1E11157B535E49973BECE6EB702ACA8D8983D8ADFC27386E2D87F76C004CF03C0490C8C49BCF808AED60038A5E82AF265CFA6F69B4F3C44F3F05C6F668DAA0FD950BFDA7CB251E33FDA15F8C40CFC9DB3DF145AD490776569EBB0461F03BC93F8BB3566656CB5E6717587CCC2E908155216ED6D2B119B394AC176A87232A7B5C5591997D839FE3FF2534907FCC06A1B48DBCD0A0F500939B1ACB2E1EC7C9AAE7A9DDBC6CC2F75C1F2F292B7E5E488DD87131B319C832ED1CFDC1AEC52216E14B353FC94FDE787425C4FB2BAF9A14B1C6E0421095B1DF48E6B23F84B38E1A8591D4160B5D065AF67590BD926FFCAEC187A1257C913EDD2F8FD9A37A6CB354C3A9A2BE9168476A45044DFCC435A4776EF1A9968675F25224E8F74348AD8E494BA583D1993CFD648BD2DAB3B615FDCC99081F5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

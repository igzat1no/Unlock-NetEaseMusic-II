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
    browser.add_cookie({"name": "MUSIC_U", "value": "003DB816DBEA22459745BB1AA45696C3C1DCEE0783E108F342CEEBCB585C7E8CC09375AFACE66F57C0AE2C5AAABDD492DF5CD54C3AAD91F6B9E0E5E9868D3937949C19A8740747AFCF9A20B96B654CA416894356C73BC37191E662D29B4C97984C8139083A3E27C85AF981213E7917266132F7F314A5428EECF289B9923481679EBDD9CEEEE27AA1A3A260360B61A6AE058CBD1262B7322D5D7A4239BF20EC446222EEAA800A0FC2F2235F2EF548E4A8F91E471869FCFB5C1520AEF8A56112A036B5EFEE548F12EE4CF84E743E07DE8D9F662F9A026412AF89B8568435039CBD5E245FBCE2E365180DA9D141FFDACD0F031E241DF0757FCDB32267B3EB5FF399437844E71D02F3A8E3CDBAEE78871BB926FB4A45A0522B7A32181F016978C5D52DEB276A17AE631011E49C5DE38F8E780C2305D58108C89D7F56CA94118A98C72D59A31A79AD7693D9BA6DD9DC1A0A267012BF3DFF39A5A063DDA9565ED09CB136"})
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

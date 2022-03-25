import datetime
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.constants import group_web_links_list

# Install chromedriver - https://chromedriver.chromium.org/downloads
# To get the executable path of google chrome - chrome://version/
# Executable path for MacOS Google Chrome - /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
# To run chrome from terminal, execute above command i.e., executable path of chrome

# Problem statement - We want to take screenshot from telegram, chromedriver launches new chrome window everytime and
# hence we need to login to tg everytime, so the ss is taken of login screen.
# Solution - Open chromedriver into existing browser where tg is once logged in already. To do that we need to launch
# chrome at some unused open port & keep opening on the same browser from code.

# To launch chrome at some specific port -
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile" at some new profile in terminal.
# Followed by - DevTools listening on ws://127.0.0.1:9222/devtools/browser/29e5bf97-6a09-4915-9e64-3a91deda4ee3
# Verify curl 127.0.0.1:9222 if chrome is running on port 9222
# It open a new browser with new profile, login tg in it, followed by hitting code script.

DRIVER = os.getenv('DRIVER_PATH')
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
group_links_list = group_web_links_list
for group_link in group_links_list:
    driver.get(group_link)
    time.sleep(10)
    file_name = '/screenshots/ss' + datetime.datetime.now().strftime("%H:%M:%S") + '.png'
    screenshot = driver.save_screenshot(file_name)
driver.quit()

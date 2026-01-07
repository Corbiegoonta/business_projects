import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_chrome_profile_path():
    system = platform.system()

    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif system == "Linux":
        return os.path.expanduser("~/.config/google-chrome")
    else:
        raise Exception("Unsupported OS")

# Detect Chrome profile
user_data_dir = get_chrome_profile_path()

options = Options()
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument("profile-directory=Default")  # Change if you use Profile 1, Profile 2, etc.

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

print("✅ Selenium is using your existing Chrome profile")

# Example: Send message to a group
time.sleep(5)
group_name = "Test"
msg = "Hello from Selenium with auto-detected profile!"

search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.send_keys(group_name)
time.sleep(2)
search_box.send_keys(Keys.ENTER)

msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
msg_box.send_keys(msg)
msg_box.send_keys(Keys.ENTER)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import os
import re
import requests
import zipfile
import shutil
import subprocess
import sys


def ensure_chromedriver():
    try:
        # Step 1: Find local Chrome version
        if sys.platform == 'win32':
            result = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                capture_output=True, text=True, shell=True
            )
            match = re.search(r"Version\s+REG_SZ\s+([\d.]+)", result.stdout, re.IGNORECASE)
            if match:
                chrome_version = match.group(1)
            else:
                raise Exception("Could not detect Chrome version on Windows.")
        else:
            # MacOS / Linux
            result = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True, text=True
            )
            match = re.search(r"Google Chrome ([\d.]+)", result.stdout)
            if match:
                chrome_version = match.group(1)
            else:
                raise Exception("Could not detect Chrome version on Mac/Linux.")

        print(f"[+] Detected Chrome version: {chrome_version}")
        major_version = chrome_version.split('.')[0]

        # Step 2: Check if chromedriver.exe exists
        if os.path.exists('chromedriver.exe'):
            print("[+] Chromedriver already exists in folder.")
            return True

        print("[*] Chromedriver not found. Preparing to download...")

        # Step 3: Get correct Chromedriver version
        latest_release_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        response = requests.get(latest_release_url)

        if "NoSuchKey" in response.text or response.status_code != 200:
            print(f"[-] No specific Chromedriver found for version {major_version}.")
            print("[*] Falling back to latest stable Chromedriver...")
            response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        
        driver_version = response.text.strip()
        print(f"[+] Using Chromedriver version: {driver_version}")

        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"

        # Step 4: Download Chromedriver
        zip_path = os.path.join(os.getcwd(), "chromedriver.zip")
        print(f"[*] Downloading chromedriver.zip to: {zip_path}")

        with open(zip_path, 'wb') as file:
            file.write(requests.get(download_url).content)

        # Step 5: Extract Chromedriver
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        print(f"[+] Chromedriver extracted successfully at: {os.getcwd()}")

        # Step 6: Clean up
        os.remove(zip_path)
        print("[+] Temporary zip deleted.")

        return True

    except Exception as e:
        print(f"[-] Failed to setup Chromedriver: {e}")
        return False


if ensure_chromedriver():
    print("Chromedriver ready to use!")
    chrome_options = Options()
    
    # 🚫 Block notifications
    prefs = {
        "profile.default_content_setting_values.notifications": 2  # 1 = Allow, 2 = Block
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

def element_exists(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        print (f"{value} exists!")
        return True
    except TimeoutException:
        print (f"{value} doesn't exist!")
        return False


def click_if_exists(driver, by, value, timeout=10):
    if element_exists(driver, by, value, timeout):
        element = driver.find_element(by, value)
        element.click()
        print(f"{value} clicked!")
    else:
        print(f"{value} not found!")

driver.get("https://sports.bet9ja.com/mobile/login")
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# 1️⃣ Wait for username field and type in username
username_field = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
)
username_field.send_keys("Bet9jaweb8")  # ✍️ Replace with your username
print("[+] Entered username!")


password_field = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))
)
password_field.send_keys("Newpassword1")  # ✍️ Replace with your password
print("[+] Entered password!")


# 2️⃣ Wait for login button and click it
login_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.w-full.mt15"))
)
login_button.click()
print("[+] Clicked login button!")


# Wait until the element is clickable
span = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iconslider_1549_league_element"]/div/div[1]/span')))
# Click the span
span.click()
print("[+] Clicked virtual league button!")


# Wait until the image is clickable
premier_league = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'select_premier')))
# Click the image
premier_league.click()
print("[+] Clicked Premier league button!")



# Wait for iframe
iframe = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
)
# Switch into iframe
driver.switch_to.frame(iframe)
# Find and click the menu button
element = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "icon-menu"))
)
driver.execute_script("arguments[0].click();", element)
print("[+] Menu button clicked!")

# (Optional) Switch back to main page tested and wasn't needed for the webpage
#driver.switch_to.default_content()


result_bttn = wait.until(EC.element_to_be_clickable((By.ID, 'a_bet_results')))
result_bttn.click()

#click to bet
bet_bttn = wait.until(EC.element_to_be_clickable((By.ID, 'a_bet_bet')))
bet_bttn.click()

# Usage example:
# click_if_exists(driver, By.CLASS_NAME, 'fa fa-bars icon-menu') #click




# 🖐️ Keep browser open until user types 'exit'
while True:
    command = input("Type 'exit' to close the browser: ").strip().lower()
    if command == "exit":
        print("[*] Exiting and closing the browser...")
        driver.quit()
        break

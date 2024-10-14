import requests
import os
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
import json
import random
import string
import time
from datetime import datetime, timedelta
import zipfile
import re

# Don"t delete or change the script function below!
with open('config.js', 'r') as f:
    content = f.read()
content = content.replace('export const config =', '').strip().rstrip(';')
config = json.loads(content)
    
def generate_random_string(length):
    if length < 8:
        raise ValueError(" Make sure the string length includes 8 digits.")
        
    vowels = "aiueo"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    digits = string.digits
    
    num_digits = 4
    remaining_length = length - num_digits
    
    num_vowels = (remaining_length + 1) // 2
    num_consonants = remaining_length // 2

    result = []
    for _ in range(num_vowels):
        result.append(random.choice(vowels))
        if len(result) < remaining_length:
            result.append(random.choice(consonants))
            
    result.extend(random.choice(digits) for _ in range(num_digits))

    return "".join(result)

def generate_random_name(length):
    if length < 5:
        raise ValueError(" Make sure the name string length includes 5 digits.")
        
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    digits = string.digits
    
    num_digits = 0
    remaining_length = length - num_digits
    
    num_vowels = (remaining_length + 1) // 2
    num_consonants = remaining_length // 2

    result = []
    for _ in range(num_vowels):
        result.append(random.choice(vowels))
        if len(result) < remaining_length:
            result.append(random.choice(consonants))
            
    result.extend(random.choice(digits) for _ in range(num_digits))

    return "".join(result)

def generate_random_date():
    day = random.randint(1, 15)
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month = random.choice(months)
    year = random.randint(1998, 2002)
    
    return {
        "day": f"{day:02d}",
        "month": month,
        "year": str(year)
    }

def select_gender(driver):
    try:
        gender_select = Select(driver.find_element(By.ID, "gender"))
        gender_select.select_by_value(str(random.randint(1, 3)))
        time.sleep(2)
    except Exception as e:
        print("Gender dropdown not found.")
        
def input_username(driver, random_email):
    try:
        create_a_gmail_address = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create a Gmail address')]"))
        )
        create_a_gmail_address.click()
        time.sleep(2)
        click_button(driver, "//span[text()='Next']")
    except TimeoutException:
        print("The option Create a Gmail address was not found.")
        
    try:
        create_your_own_email = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create your own Gmail address')]"))
        )
        create_your_own_email.click()
        time.sleep(2)
    except TimeoutException:
        print("The option Create your own Gmail address was not found.")
        
    try:
        email_field = driver.find_element(By.NAME, "Username")
        email_field.send_keys(random_email)
        time.sleep(2)
    except Exception as e:
        print("The field for email was not found.")
    click_button(driver, "//span[text()='Next']")

def click_button(driver, path_element):
    try:
        driver.find_element(By.XPATH, path_element).click()
    except Exception as e:
        print("The button was not found.")
    time.sleep(10)
    
def check_valid_api():
    if config['otp_provider'].upper() in ["SIOTP", "SIOTPUNL"]:
        response = requests.get(
            f"https://siotp.com/api/getbalance?apikey={config['api_key']}"
        )
        response_data = response.json()
        try:
            if response_data["status"] == "success":
                print("Valid api key.")
            else:
                raise ValueError
        except ValueError:
            print("Invalid api key.")
            print("Wait 10 seconds before this error message is automatically closed.")
            time.sleep(10)
            sys.exit(1)   
    elif config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        response = requests.get(
            f"https://tokoclaude.com/api/get-profile/{config['api_key']}"
        )
        if response.status_code == 201:
            response_data = response.json()
            try:
                if response_data["success"]:
                    print("Valid api key.")
                else:
                    raise ValueError
            except ValueError:
                print("Invalid api key.")
                print("Wait 10 seconds before this error message is automatically closed.")
                time.sleep(10)
                sys.exit(1)
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        response = requests.get(
            f"https://turbootp.com/api/get-profile/{config['api_key']}"
        )
        if response.status_code == 201:
            response_data = response.json()
            try:
                if response_data["success"]:
                    print("Valid api key.")
                else:
                    raise ValueError
            except ValueError:
                print("Invalid api key.")
                print("Wait 10 seconds before this error message is automatically closed.")
                time.sleep(10)
                sys.exit(1)
    else:
        response = requests.get(
            "https://5sim.net/v1/user/profile",
            headers={"Authorization": f"Bearer {config['api_key']}"}
        )
        if response.status_code == 200:
            print("Valid api key.")
        else:
            print("Invalid api key.")
            print("Wait 10 seconds before this error message is automatically closed.")
            time.sleep(10)
            sys.exit(1)
    
def get_product_id():
    if config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        response = requests.get(
            f"https://tokoclaude.com/api/get-services/{config['api_key']}"
        )
        if response.status_code == 201:
            response_data = response.json()
            try:
                if response_data["success"]:
                    for product in response_data["data"]["data"]:
                        if config['otp_provider'].upper() == "TOKOCLAUDE" and product["name"] == "Gmail / Google | Youtube":
                            product_id = product["id"]
                            break
                        elif config['otp_provider'].upper() == "TOKOCLAUDEUNL" and product["name"] == "Gmail / Google | Youtube ( UNLIMITED )":
                            product_id = product["id"]
                            break
                    return product_id
                else:
                    raise ValueError
            except ValueError:
                print("Failed to get product id.")
                return None, None
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
            return None, None
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        response = requests.get(
            f"https://turbootp.com/api/get-services/{config['api_key']}"
        )
        if response.status_code == 201:
            response_data = response.json()
            try:
                if response_data["success"]:
                    for product in response_data["data"]["data"]:
                        if config['otp_provider'].upper() == "TURBOOTP" and product["name"] == "Gmail / Google | Youtube":
                            product_id = product["id"]
                            break
                        elif config['otp_provider'].upper() == "TURBOOTPUNL" and product["name"] == "Gmail / Google | Youtube ( UNLIMITED )":
                            product_id = product["id"]
                            break
                    return product_id
                else:
                    raise ValueError
            except ValueError:
                print("Failed to get product id.")
                return None, None
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:")
            print(response.text)
            return None, None
    
def get_phone_number(product_id):
    if config['otp_provider'].upper() in ["SIOTP", "SIOTPUNL"]:
       while True:
            if config['otp_provider'].upper() == "SIOTPUNL":
                response = requests.get(
                    f"https://siotp.com/api/order?apikey={config['api_key']}&service=351&operator={config['phone_number_operator']}&country={config['phone_number_country']}"
                )
            else:
                response = requests.get(
                    f"https://siotp.com/api/order?apikey={config['api_key']}&service=2&operator={config['phone_number_operator']}&country={config['phone_number_country']}"
                )
            response_data = response.json()
            if response_data["status"] == "success":
                try:
                    activation_id = response_data["id"]
                    phone_number = response_data["number"]
                    if phone_number.startswith("0"):
                        phone_number = "+62" + phone_number[1:]
                    else:
                        phone_number = "+" + phone_number
                    return activation_id, phone_number
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    continue
            else:
                print(response_data["message"])
                continue
    elif config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        while True:
            response = requests.get(
                f"https://tokoclaude.com/api/set-orders/{config['api_key']}/{product_id}"
            )
            if response.status_code == 201:
                response_data = response.json()
                if response_data["success"]:
                    try:
                        activation_id = response_data["data"]["data"]["order_id"]
                        phone_number = response_data["data"]["data"]["number"]
                        if phone_number.startswith("0"):
                            phone_number = "+62" + phone_number[1:]
                        return activation_id, phone_number
                    except ValueError:
                        print("Failed to parse JSON. Fill in the response:")
                        print(response.text)
                        continue
                else:
                    if response_data["data"]["messages"] == "Number Empty":
                        print(response_data["data"]["messages"])
                        time.sleep(config['number_empty_cooldown'])
                    else:
                        print(response_data["data"]["messages"])
                        time.sleep(10)
                    continue
            else:
                print("Failed to get phone number.")
                time.sleep(10)
                continue
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        while True:
            response = requests.get(
                f"https://turbootp.com/api/set-orders/{config['api_key']}/{product_id}"
            )
            if response.status_code == 201:
                response_data = response.json()
                if response_data["success"]:
                    try:
                        activation_id = response_data["data"]["data"]["order_id"]
                        phone_number = response_data["data"]["data"]["number"]
                        if phone_number.startswith("0"):
                            phone_number = "+62" + phone_number[1:]
                        return activation_id, phone_number
                    except ValueError:
                        print("Failed to parse JSON. Fill in the response:")
                        print(response.text)
                        continue
                else:
                    if response_data["data"]["messages"] == "Number Empty":
                        print(response_data["data"]["messages"])
                        time.sleep(config['number_empty_cooldown'])
                    else:
                        print(response_data["data"]["messages"])
                        time.sleep(10)
                    continue
            else:
                print("Failed to get phone number.")
                time.sleep(10)
                continue
    else:
        while True:
            response = requests.get(
                "https://5sim.net/v1/user/buy/activation/" + (config['phone_number_country'].lower()) + "/" + (config['phone_number_operator'].lower()) + "/google",
                headers={"Authorization": f"Bearer {config['api_key']}"}
            )
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    activation_id = response_data["id"]
                    phone_number = response_data["phone"]
                    return activation_id, phone_number
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    continue
            else:
                print("Failed to get phone number.")
                time.sleep(10)
                continue

def cancel_phone_number(activation_id):
    if config['otp_provider'].upper() in ["SIOTP", "SIOTPUNL"]:
        time.sleep(65)
        response = requests.get(
            f"https://siotp.com/api/changestatus?apikey={config['api_key']}&id={activation_id}&status=0"
        )
        response_data = response.json()
        if response_data["status"] == "success":
            try:
                status = "Cancelled"
                print(f"Status: {status}")
            except ValueError:
                print("Failed to parse JSON. Fill in the response:")
                print(response.text)
                return None, None
        else:
            print("Failed to cancel the phone number.")
            return None, None
    elif config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        response = requests.get(
            f"https://tokoclaude.com/api/cancle-orders/{config['api_key']}/{activation_id}"
        )
        if response.status_code == 201:
            response_data = response.json()
            if response_data["success"]:
                try:
                    status = response_data["data"]["messages"]
                    print(f"Status: {status}")
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    return None, None
            else:
                print("Failed to cancel the phone number.")
                return None, None
        else:
            print("Failed to cancel the phone number.")
            return None, None
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        response = requests.get(
            f"https://turbootp.com/api/cancle-orders/{config['api_key']}/{activation_id}"
        )
        if response.status_code == 201:
            response_data = response.json()
            if response_data["success"]:
                try:
                    status = response_data["data"]["messages"]
                    print(f"Status: {status}")
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    return None, None
            else:
                print("Failed to cancel the phone number.")
                return None, None
        else:
            print("Failed to cancel the phone number.")
            return None, None
    else:
        response = requests.get(
            f"https://5sim.net/v1/user/ban/{activation_id}",
            headers={"Authorization": f"Bearer {config['api_key']}"}
        )
        if response.status_code == 200:
            try:
                response_data = response.json()
                status = response_data["status"]
                print(f"Status: {status}")
            except ValueError:
                print("Failed to parse JSON. Fill in the response:")
                print(response.text)
                return None, None
        else:
            print("Failed to cancel the phone number.")
            return None, None
    
def get_otp(activation_id):
    scan_otp = 0
    if config['otp_provider'].upper() in ["SIOTP", "SIOTPUNL"]:
        while True:
            response = requests.get(
                f"https://siotp.com/api/getotp?apikey={config['api_key']}&id={activation_id}"
            )
            response_data = response.json()
            if response_data["status"] == "success":
                if 60 > scan_otp:
                    scan_otp = scan_otp + 1
                    if response_data["data"]["status"] == "3":
                        try:
                            sms = response_data["data"]["inbox"]
                            if sms:
                                return sms
                        except ValueError:
                            print("Failed to parse JSON. Fill in the response:")
                            print(response.text)
                            return None, None
                    time.sleep(1)
                else:
                    print("Failed to get OTP.")
                    cancel_phone_number(activation_id)
                    driver.quit()
                    return None, None
            else:
                print("Failed to get OTP.")
                return None, None
    elif config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        while True:
            response = requests.get(
                f"https://tokoclaude.com/api/get-orders/{config['api_key']}/{activation_id}"
            )
            if response.status_code == 201:
                response_data = response.json()
                if response_data["success"]:
                    if 60 > scan_otp:
                        scan_otp = scan_otp + 1
                        try:
                            sms = response_data["data"]["data"][0]["sms"]
                            if sms:
                                return re.search(r"\d+", sms).group()
                        except ValueError:
                            print("Failed to parse JSON. Fill in the response:")
                            print(response.text)
                            return None, None
                        time.sleep(1)
                    else:
                        print("Failed to get OTP.")
                        cancel_phone_number(activation_id)
                        driver.quit()
                        return None, None
                else:
                    print("Failed to get OTP.")
                    return None, None
            else:
                print("Failed to get OTP.")
                return None, None
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        while True:
            response = requests.get(
                f"https://turbootp.com/api/get-orders/{config['api_key']}/{activation_id}"
            )
            if response.status_code == 201:
                response_data = response.json()
                if response_data["success"]:
                    if 60 > scan_otp:
                        scan_otp = scan_otp + 1
                        try:
                            response_data = response.json()
                            sms = response_data["data"]["data"][0]["sms"]
                            if sms:
                                return re.search(r"\d+", sms).group()
                        except ValueError:
                            print("Failed to parse JSON. Fill in the response:")
                            print(response.text)
                            return None, None
                        time.sleep(1)
                    else:
                        print("Failed to get OTP.")
                        cancel_phone_number(activation_id)
                        driver.quit()
                        return None, None
                else:
                    print("Failed to get OTP.")
                    return None, None
            else:
                print("Failed to get OTP.")
                return None, None
    else:
        while True:
            response = requests.get(
                f"https://5sim.net/v1/user/check/{activation_id}",
                headers={"Authorization": f"Bearer {config['api_key']}"}
            )
            if response.status_code == 200:
                if 60 > scan_otp:
                    scan_otp = scan_otp + 1
                    try:
                        response_data = response.json()
                        if "sms" in response_data and len(response_data["sms"]) > 0:
                            return response_data["sms"][0]["code"]
                    except ValueError:
                        print("Failed to parse JSON. Fill in the response:")
                        print(response.text)
                        return None, None
                    time.sleep(1)
                else:
                    print("Failed to get OTP.")
                    cancel_phone_number(activation_id)
                    driver.quit()
                    return None, None
            else:
                print("Failed to get OTP.")
                return None, None        

def finish_order(activation_id):
    if config['otp_provider'].upper() in ["SIOTP", "SIOTPUNL"]:
        response = requests.get(
            f"https://siotp.com/api/changestatus?apikey={config['api_key']}&id={activation_id}&status=1"
        )
        response_data = response.json()
        if response_data["status"] == "success":
            try:
                status = "Finished"
                print(f"Status: {status}")
            except ValueError:
                print("Failed to parse JSON. Fill in the response:")
                print(response.text)
                return None, None
        else:
            print("failed to finish phone number.")
            return None, None
    elif config['otp_provider'].upper() in ["TOKOCLAUDE", "TOKOCLAUDEUNL"]:
        response = requests.get(
            f"https://tokoclaude.com/api/finish-orders/{config['api_key']}/{activation_id}"
        )
        if response.status_code == 201:
            response_data = response.json()
            if response_data["success"]:
                try:
                    status = response_data["data"]["messages"]
                    print(f"Status: {status}")
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    return None, None
            else:
                print("failed to finish phone number.")
                return None, None
        else:
            print("failed to finish phone number.")
            return None, None
    elif config['otp_provider'].upper() in ["TURBOOTP", "TURBOOTPUNL"]:
        response = requests.get(
            f"https://turbootp.com/api/finish-orders/{config['api_key']}/{activation_id}"
        )
        if response.status_code == 201:
            response_data = response.json()
            if response_data["success"]:
                try:
                    status = response_data["data"]["messages"]
                    print(f"Status: {status}")
                except ValueError:
                    print("Failed to parse JSON. Fill in the response:")
                    print(response.text)
                    return None, None
            else:
                print("failed to finish phone number.")
                return None, None
        else:
            print("failed to finish phone number.")
            return None, None
    else:
        response = requests.get(
            f"https://5sim.net/v1/user/finish/{activation_id}",
            headers={"Authorization": f"Bearer {config['api_key']}"}
        )
        if response.status_code == 200:
            try:
                response_data = response.json()
                status = response_data["status"]
                print(f"Status: {status}")
            except ValueError:
                print("Failed to parse JSON. Fill in the response:")
                print(response.text)
                return None, None
        else:
            print("failed to finish phone number.")
            return None, None

def get_user_profile(email):
    user_profile_dir = os.path.abspath(f"User_Data/{email}")
    os.makedirs(user_profile_dir, exist_ok=True)
    return user_profile_dir
        
def webhook_date():
    time_difference = timedelta(hours=7)
    current_time_GMT = datetime.utcnow()
    current_time_webhook = current_time_GMT + time_difference
    formatted_time = current_time_webhook.strftime("%A, %B %d, %Y | %H:%M") + " [GMT+7]"
    return formatted_time
    
def discord_webhook(content):
    if config['discord_url'] != "":
        data = {
            "username": "Grow King Scripts",
            "avatar_url": "https://media.discordapp.net/attachments/1151744897687224320/1160427676654391428/GKS_Logo.jpg?ex=65349f7d&is=65222a7d&hm=b11ee741e5b45e61d96257712224c5ad4c5c44e4e42fde4e441c529a646a708c&=&width=427&height=427",
            "embeds": [
                {
                    "image": {
                        "url": "https://media.discordapp.net/attachments/1151744897687224320/1160427676381741106/GKS_Footer.jpg?ex=65349f7d&is=65222a7d&hm=3e4925cc5fb2ba188bf8c6c4ae7cc58aeca7ca1507011b923c8500e1aa70eb8b&="
                    },
                    "title": "GKS Gmail Creator \nBy **Grow King Scripts**",
                    "description": f"{content}",
                    "color": 15105570,
                    "footer": {
                        "text": "GKS Gmail Creator \n" + webhook_date()
                    }
                }
            ]
        }
        
        result = requests.post(config['discord_url'], json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print(f"Discord webhook successfully sent.")
    
def create_gmail_account(index, max_thread):
    proxy_value = 0
    while True:
        if config['webdriver'].upper() == "RANDOM":
            webdriver_list = ["CHROME", "EDGE", "FIREFOX"]
            webdriver_name = random.choice(webdriver_list).upper()
        elif config['webdriver'].upper() != "RANDOM":
            webdriver_name = config['webdriver'].upper()
        print("Webdriver: " + webdriver_name)
        random_email = generate_random_string(10)
        random_first_name = generate_random_name(5)
        random_last_name = generate_random_name(5)
        random_password = "@" + generate_random_string(9)
        random_date = generate_random_date()
        
        # Selenium webdriver configuration
        if webdriver_name == "CHROME":
            if os.path.exists(os.path.abspath("WebDriver/Chrome/chromedriver.exe")) and os.path.exists(os.path.abspath("WebDriver/Chrome/chrome.exe")):
                webdriver_exe = os.path.abspath("WebDriver/Chrome/chromedriver.exe")
                service = ChromeService(executable_path=webdriver_exe)
                options = ChromeOptions()
                options.binary_location = os.path.abspath("WebDriver/Chrome/chrome.exe")
            else:
                print("chromedriver.exe or chrome.exe is not found in the WebDriver/Chrome folder.")
                print("Wait 10 seconds before this error message is automatically closed.")
                time.sleep(10)
                sys.exit(1)
        elif webdriver_name == "EDGE":
            if os.path.exists(os.path.abspath("WebDriver/Edge/msedgedriver.exe")) and os.path.exists(os.path.abspath("WebDriver/Edge/msedge.exe")):
                webdriver_exe = os.path.abspath("WebDriver/Edge/msedgedriver.exe")
                service = EdgeService(executable_path=webdriver_exe)
                options = EdgeOptions()
                options.binary_location = os.path.abspath("WebDriver/Edge/msedge.exe")
            else:
                print("msedgedriver.exe or msedge.exe is not found in the WebDriver/Edge folder.")
                print("Wait 10 seconds before this error message is automatically closed.")
                time.sleep(10)
                sys.exit(1)
        elif webdriver_name == "FIREFOX":
            if os.path.exists(os.path.abspath("WebDriver/Mozilla Firefox/geckodriver.exe")) and os.path.exists(os.path.abspath("WebDriver/Mozilla Firefox/firefox.exe")):
                webdriver_exe = os.path.abspath("WebDriver/Mozilla Firefox/geckodriver.exe")
                service = FirefoxService(executable_path=webdriver_exe)            
                options = FirefoxOptions()
                options.binary_location = os.path.abspath("WebDriver/Mozilla Firefox/firefox.exe")
            else:
                print("geckodriver.exe or firefox.exe is not found in the WebDriver/Mozilla Firefox folder.")
                print("Wait 10 seconds before this error message is automatically closed.")
                time.sleep(10)
                sys.exit(1)
                
        if webdriver_name in ["CHROME", "EDGE"]:
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--disable-blink-features=AutomationControlled")
            user_profile = get_user_profile(f"{random_email}@gmail.com")
            options.add_argument(f"user-data-dir={user_profile}")
            options.add_argument("--lang=en-EN")
            if config['fake_useragent_mode']:
                ua = UserAgent()
                user_agent = ua.random
                print(user_agent)
                options.add_argument(f"--user-agent={user_agent}")
            if config['headless_mode']:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
            if webdriver_name == "CHROME":
                if config['proxies'][proxy_value] == "":
                    proxy_host, proxy_port, proxy_user, proxy_pass = "", "", "", ""
                    print("Current IP is " + requests.get("https://ipv4.webshare.io/").text)
                    print("Status: Proxy is not in use.")
                else:
                    split_proxy = config['proxies'][proxy_value].split(":")
                    proxy_host = split_proxy[0] if len(split_proxy) > 0 else ""
                    proxy_port = split_proxy[1] if len(split_proxy) > 1 else ""
                    proxy_user = split_proxy[2] if len(split_proxy) > 2 else ""
                    proxy_pass = split_proxy[3] if len(split_proxy) > 3 else ""
                    
                    manifest_json = """
                    {
                        "version": "0.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

                    background_js = f"""
                    var config = {{
                        mode: "fixed_servers",
                        rules: {{
                            singleProxy: {{
                                scheme: "http",
                                host: "{proxy_host}",
                                port: parseInt({proxy_port})
                            }},
                            bypassList: ["localhost"]
                        }}
                    }};

                    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

                    function callbackFn(details) {{
                        return {{
                            authCredentials: {{
                                username: "{proxy_user}",
                                password: "{proxy_pass}"
                            }}
                        }};
                    }}

                    chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {{urls: ["<all_urls>"]}},
                        ["blocking"]
                    );
                    """
                    proxy_auth = "proxy_auth_plugin.zip"
                    with zipfile.ZipFile(proxy_auth, "w") as zp:
                        zp.writestr("manifest.json", manifest_json)
                        zp.writestr("background.js", background_js)
                    options.add_extension(proxy_auth)
                    print("Current IP is " + proxy_host + " \nStatus: Proxy is in use.")
                    proxy_value += 1
                    if proxy_value > (len(config['proxies']) - 1):
                        proxy_value = 0
            elif webdriver_name == "EDGE":
                proxy_host, proxy_port, proxy_user, proxy_pass = "", "", "", ""
                print("Current IP is " + requests.get("https://ipv4.webshare.io/").text)
                print("Status: Proxy is not in use.")
        elif webdriver_name == "FIREFOX":
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("useAutomationExtension", False)
            user_profile = get_user_profile(f"{random_email}@gmail.com")
            options.set_preference("profile", user_profile)
            options.set_preference("intl.accept_languages", "en-EN")
            if config['fake_useragent_mode']:
                ua = UserAgent()
                user_agent = ua.random
                print(user_agent)
                options.set_preference("general.useragent.override", user_agent)
            if config['headless_mode']:
                options.add_argument("--headless")
                options.set_preference("browser.tabs.remote.autostart", False)
            proxy_host, proxy_port, proxy_user, proxy_pass = "", "", "", ""
            print("Current IP is " + requests.get("https://ipv4.webshare.io/").text)
            print("Status: Proxy is not in use.")
        
        if webdriver_name == "CHROME":
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_window_size(300, 600)
        elif webdriver_name == "EDGE":
            driver = webdriver.Edge(service=service, options=options)
            driver.set_window_size(300, 600)
        elif webdriver_name == "FIREFOX":
            driver = webdriver.Firefox(service=service, options=options)
            driver.set_window_size(300, 600)
            
        try:
            # Step 1: Go to the Gmail signup page
            driver.get("https://accounts.google.com/signup")
            
            # Step 2: Input the name
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.NAME, "firstName"))
                )
                
                driver.find_element(By.NAME, "firstName").send_keys(random_first_name)
                time.sleep(2)
                driver.find_element(By.NAME, "lastName").send_keys(random_last_name)
                time.sleep(2)
                click_button(driver, "//span[text()='Next']")
            except TimeoutException:
                print(f"The field for first name was not found.")
                driver.quit()
                continue
                
            # Step 3: Set birth date and gender
            while True:
                try:
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.ID, "day"))
                    )
                    
                    driver.find_element(By.ID, "day").send_keys(random_date["day"])
                    time.sleep(2)
                    driver.find_element(By.ID, "month").send_keys(random_date["month"])
                    time.sleep(2)
                    driver.find_element(By.ID, "year").send_keys(random_date["year"])
                    time.sleep(2)
                    select_gender(driver)
                    click_button(driver, "//span[text()='Next']")
                    break
                except TimeoutException:
                    print("The field for birthday was not found.")
                    continue
                
            # Step 4: Check how to sign in, input the username, password, and phone number
            input_username(driver, random_email)
            while True:
                try:
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.NAME, "Passwd"))
                    )
                    driver.find_element(By.NAME, "Passwd").send_keys(random_password)
                    time.sleep(2)
                    driver.find_element(By.NAME, "PasswdAgain").send_keys(random_password)
                    time.sleep(2)
                    click_button(driver, "//span[text()='Next']")
                    break
                except TimeoutException:
                    print("The field for password was not found.")
                    continue
                
            try:
                input_phone_number = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "phoneNumberId"))
                )
                product_id = get_product_id()
                activation_id, phone_number = get_phone_number(product_id)
                input_phone_number.send_keys(phone_number)
                time.sleep(2)
                click_button(driver, "//span[text()='Next']")
            except TimeoutException:
                print("The field for phone numbers was not found.")
                driver.quit()
                continue
                
            try:
                otp_field = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.NAME, "code"))
                )
                otp = get_otp(activation_id)
                otp_field.send_keys(otp)
                time.sleep(2)
                click_button(driver, "//span[text()='Next']")
                finish_order(activation_id)
            except TimeoutException:
                print("The OTP page does not display.")
                cancel_phone_number(activation_id)
                driver.quit()
                continue
                    
            # Step 5: Process completion
            while True:
                if config['recovery_email']:
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.NAME, "recovery"))
                        )
                        driver.find_element(By.NAME, "recovery").send_keys(config['recovery_email'])
                        time.sleep(2)
                        click_button(driver, "//span[text()='Next']")
                        break
                    except TimeoutException:
                        print("The email recovery page does not display.")
                        continue
                else:
                    click_button(driver, "//span[text()='Skip']")
                    break
            
            while True:
                try:
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Review your account info')]"))
                    )
                    click_button(driver, "//span[text()='Next']")
                    break
                except TimeoutException:
                    print("Waiting...")
                    continue
                    
            while True:
                try:
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Privacy and Terms')]"))
                    )
                    click_button(driver, "//span[text()='I agree']")
                    break
                except TimeoutException:
                    print("Waiting...")
                    continue
                    
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Confirm']"))
                )
                click_button(driver, "//span[text()='Confirm']")
            except TimeoutException:
                print("The Confirm button does not found.")
            
            while True:
                try:
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome,')]"))
                    )
                    
                    with open("gmail_results.txt", "a") as f:
                        if config['recovery_email']:
                            f.write(f"{random_email}@gmail.com|{random_password}|" + (config['recovery_email']) + "\n")
                            discord_webhook(f"Gmail account created successfully: \n{random_email}@gmail.com|{random_password}|" + (config['recovery_email']))
                            print(f"Gmail account created successfully: {random_email}@gmail.com|{random_password}|" + (config['recovery_email']))
                        else:
                            f.write(f"{random_email}@gmail.com|{random_password}\n")
                            discord_webhook(f"Gmail account created successfully: \n{random_email}@gmail.com|{random_password}")
                            print(f"Gmail account created successfully: {random_email}@gmail.com|{random_password}")
                    break
                except TimeoutException:
                    print("Account failed to create.")
            time.sleep(10)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Wait 10 seconds before this error message is automatically closed.")
            time.sleep(10)
            driver.quit()
            continue
        finally:
            driver.quit()

def run_multiple_threads(max_thread):
    threads = []
    for i in range(max_thread):
        t = threading.Thread(target=create_gmail_account, args=(i, max_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

check_valid_api()
for _ in range(config['max_accounts_created_per_thread']):
    run_multiple_threads(config['max_thread'])
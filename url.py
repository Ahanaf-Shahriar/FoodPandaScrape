import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def url_request():
    url = "https://hungrynaki.com/restaurants"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Website is accessible.")
        else:
            print("Website is not accessible. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def chromium_driver():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome()
    while(True):
        pass

        return driver.get("https://hungrynaki.com/restaurant/diggger-mohakhali/menu")
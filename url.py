import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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


def restaurant_url():
    restaurant_urls = []
    restaurant_names = []

    with open('restaurant_names.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) > 0:
                restaurant_urls.append(row[1])

    print(restaurant_urls)


    return restaurant_urls

def test():
    # Set up Selenium WebDriver
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the webpage
        driver.get("https://www.foodpanda.com.bd/restaurant/s0hh/gloria-jeans-coffee-gulshan-1")

        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')
        title_element = driver.find_element(By.XPATH, "//button[@data-testid='vendor-main-info-section-button']")

        # Get the text of the button element
        restaurant_name = title_element.text
        print(restaurant_name)
        # Find the container for the menu categories
        menu_category_containers = soup.find_all('ul', {'class': 'dish-list-grid'})
        num_containers = len(menu_category_containers)
        print("Number of menu_category_containers found:", num_containers)

        for container in menu_category_containers:
            button_elements = container.find_all('button', {'data-testid': 'menu-product-button-overlay-id'})
            for button_element in button_elements:
                # Get the value of the aria-label attribute
                aria_label = button_element.get('aria-label')
                # Remove the " - Add to cart" text
                aria_label = aria_label.replace(" - Add to cart", "")
                print(aria_label)

    except NoSuchElementException as e:
        print("Element not found:", str(e))

    finally:
        if driver is not None:
            driver.quit()
            print("WebDriver closed successfully.")
from telnetlib import EC
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_title():
    page = requests.get("https://hungrynaki.com/restaurant/diggger-mohakhali/menu")
    soup = BeautifulSoup(page.content, 'html.parser')
    span_names = []
    span_elements = soup.find_all('span', {'itemprop': 'name'})
    if span_elements:
        for span_element in span_elements:
            text = span_element.get_text(strip=True)
            span_names.append(text)
            #span_name[1] contains the name of the restaurant
        print(span_names[1])

    else:
        print("No matching span elements found with itemprop='name'.")






def scrape_menu():
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get("https://hungrynaki.com/restaurant/diggger-mohakhali/menu")

    # Wait for the desired element to be visible
    wait = WebDriverWait(driver, 10)  # Maximum wait time in seconds
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'item-end')))

    # Get the page source after dynamic content has loaded
    page_source = driver.page_source

    # Parse the page source with Beautiful Soup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the container for the menu categories
    item_containers = soup.find_all('div', {'class': 'menu-category-container'})
    if item_containers:
        for item_container in item_containers:
            # Find the h4 elements within the item container
            h4_elements = item_container.find_all('h4')
            # Find the p elements within the item container
            p_elements = item_container.find_all('p')
            # Find the img elements within the item container
            img_elements = item_container.find_all('img')
            # Find the span elements with class 'price' within the item container
            span_elements = item_container.find_all('span', {'class': 'price'})

            # Extract the pizza details
            item_names = []
            item_descriptions = []
            img_src_list = []
            item_prices = []

            # Iterate over the h4 elements and extract the text
            for h4_element in h4_elements:
                item_names.append(h4_element.text.strip())
            # Iterate over the p elements and extract the text
            for p_element in p_elements:
                item_descriptions.append(p_element.text.strip())
            # Iterate over the img elements and extract the src attribute
            for img_element in img_elements:
                img_src = img_element['src']
                img_src_list.append(img_src)
            # Iterate over the span elements and extract the price text
            for span_element in span_elements:
                item_prices.append(span_element.text.strip())

            # Print the extracted details
            print("Menu Category:")
            for name, description, src, price in zip(item_names, item_descriptions, img_src_list, item_prices):
                print("Name:", name)
                print("Description:", description)
                print("Image URL:", src)
                print("Price:", price)
                print()

    else:
        print("No matching menu-category-container found.")

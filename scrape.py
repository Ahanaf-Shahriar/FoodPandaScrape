import csv
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from url import restaurant_url





def scrape_restaurant_names():
    options = Options()
    #options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    try:

        driver.get("https://www.foodpanda.com.bd/restaurants/new/?lat=23.7468&lng=90.41449&vertical=restaurants&expedition=delivery")

        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

        span_elements = soup.find_all('span', class_='name fn')
        print(len(span_elements))

        restaurant_data = []

        for span_element in span_elements:
            # Extract the text content (restaurant name)
            restaurant_name = span_element.text

            # Find the parent <a> tag
            a_tag = span_element.find_parent('a')

            # Extract the href attribute value
            href = a_tag.get('href')

            # Add the restaurant name and href to the list
            restaurant_data.append([restaurant_name, href])

            # Print the scraped data
            print("Restaurant Name:", restaurant_name)
            print("Href:", href)

        # Save the restaurant names and hrefs in a CSV file
        with open('restaurant_names.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Restaurant Name', 'Href'])
            writer.writerows(restaurant_data)

    finally:
        if driver is not None:
            driver.quit()


def scrape_restaurant_page(restaurant_urls):
    # Set up Selenium WebDriver
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    options.add_argument(f"user-agent={random_user_agent}")

    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    try:
        for i in range(len(restaurant_urls)):
            url = restaurant_urls[i]
            print(url)

            full_url = "https://www.foodpanda.com.bd" + url
            print(full_url)
            driver.get(full_url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
        # Find the restaurant name element
            title_element = driver.find_element(By.XPATH, "//button[@data-testid='vendor-main-info-section-button']")
            restaurant_name = title_element.text.strip()
            print("Restaurant Name:", restaurant_name)

            # Find the containers for the menu categories

            menu_category_containers = soup.find_all('ul', class_='dish-list-grid')
            num_containers = len(menu_category_containers)
            print("Number of menu category containers found:", num_containers)

            for container in menu_category_containers:
                button_elements = container.find_all('button', {'data-testid': 'menu-product-button-overlay-id'})
                for button_element in button_elements:
                    # Get the value of the aria-label attribute
                    aria_label = button_element.get('aria-label')
                    # Remove the " - Add to cart" text
                    aria_label = aria_label.replace(" - Add to cart", "")
                    print(aria_label)
                    time.sleep(random.uniform(12, 30))

    except NoSuchElementException as e:
        print("Element not found:", str(e))

    finally:
        if driver is not None:
            driver.quit()
            print("WebDriver closed successfully.")



import csv

from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def scrape_restaurant_page():
    # Set up Selenium WebDriver
    options = Options()
    # options.add_argument('--headless')
    url = input("Enter the URL of the restaurant: ")

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the webpage
        driver.get(url)

        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the restaurant name element
        title_element = soup.find('button', {'data-testid': 'vendor-main-info-section-button'})
        restaurant_name = title_element.text.strip()
        print("Restaurant Name:", restaurant_name)

        # Find the containers for the menu categories
        menu_category_containers = soup.find_all('ul', {'class': 'dish-list-grid'})
        num_containers = len(menu_category_containers)
        print("Number of menu category containers found:", num_containers)

        for container in menu_category_containers:
            button_elements = container.find_all('button', {'data-testid': 'menu-product-button-overlay-id'})
            p_elements = container.find_all('p', {'data-testid': 'menu-product-description'})
            div_elements = container.find_all('div', {'data-testid': 'menu-product-image'})

            for button_element, p_element, div_element in zip(button_elements, p_elements, div_elements):
                # Get the value of the aria-label attribute
                aria_label = button_element.get('aria-label')
                # Remove the " - Add to cart" text
                aria_label = aria_label.replace(" - Add to cart", "")

                # Get the description text
                description = p_element.text.strip()

                # Get the dish photo URL
                style_attr = div_element.get('style')
                photo_url = style_attr.split('url("')[1].split('")')[0]

                print("Menu Item:", aria_label)
                print("Description:", description)
                print("Photo URL:", photo_url)
                print()

    except NoSuchElementException as e:
        print("Element not found:", str(e))

    finally:
        if driver is not None:
            driver.quit()
            print("WebDriver closed successfully.")

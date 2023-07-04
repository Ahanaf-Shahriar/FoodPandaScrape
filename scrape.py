import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By





def scrape_restaurant_names():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the webpage
        driver.get(
            "https://www.foodpanda.com.bd/restaurants/new/?lat=23.7468&lng=90.41449&vertical=restaurants&expedition=delivery")

        # Get the page source after dynamic content has loaded
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

        span_elements = soup.find_all('span', class_='name fn')
        print(len(span_elements))

        restaurant_names = []

        for span_element in span_elements:
            # Extract the text content
            text = span_element.text

            # Add the restaurant name to the list
            restaurant_names.append(text)

            # Print the scraped text
            print(text)

        # Save the restaurant names in a CSV file
        with open('restaurant_names.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Restaurant Names'])
            writer.writerows(zip(restaurant_names))

    finally:
        if driver is not None:
            driver.quit()



def scrape_restaurant_page():
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
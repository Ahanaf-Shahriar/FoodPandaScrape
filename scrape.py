import csv

from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options







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


def scrape_restaurant_page():
    # Set up Selenium WebDriver
    options = Options()
    #options.add_argument('--headless')

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


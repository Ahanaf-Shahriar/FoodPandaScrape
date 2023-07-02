from scrape import scrape_title,scrape_menu,scrape_restaurant_names,search_bar_interaction
from url import url_request
from selenium import  webdriver







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url_request()
    scrape_title()
    search_bar_interaction()
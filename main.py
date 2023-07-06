from scrape import scrape_restaurant_page, scrape_restaurant_names
from url import restaurant_url,test

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    restaurant_urls= restaurant_url()
    scrape_restaurant_page(restaurant_urls)
    #test()

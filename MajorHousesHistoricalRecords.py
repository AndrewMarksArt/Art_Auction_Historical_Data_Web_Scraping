import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class HistoricalAuctionRecords():
    """
    Class the will allow us to navigate to the 3 major auction house websites Sotheby's,
    Christies, and Phillips, find past auction results and grab the links to all past
    contemporary auctions, the title of the sale, and the date/time/location of the sale.
    """
    def __init__(self, chrome_driver_path):
        """
        Initialize the Historical Auction Records class and setup the Selenium webdriver.

        ----------
        Parameters
        ----------
        chrome_driver_path  :   string, path to where the chromedriver is installed
        """
        # use chrome driver path to initialize the driver
        self.driver = webdriver.Chrome(chrome_driver_path)


    def scroll_to_bottom(self):
        """
        For pages that load content dynamically as the user scrolls this allows us to
        scroll down to the bottom of the page so we can let the content we need load.
        """
        # let the user know selenium is controlling the page
        print('start scrolling')

        # scroll wait time
        wait = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # calculate where we are on page, try to scroll down, re-calculate
        # where we are on the page. If the page hasn't scrolled down we are
        # at the bottom of the page and break out of the loop.
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(wait)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def save_to_csv(self, auctions, f_name):
        """
        Takes the scraping results and saves it as a csv file.

        ----------
        Parameters
        ----------
        auctions    :   list of lists holding values from the scrape, an example
                        would be [Auction Title, Auction Date/Time/Location, Link to results]
        f_name      :   string, file name for the saved file
        """
        with open(f_name, "w", newline='') as f:
            writer = csv.writer(f)
            for row in auctions:
                writer.writerow(row)


    def phillips(self, url, save_results=True, f_name=None):
        """
        Goes to the provided url where Philips past contemporary auctions are listed, scrape
        the Auction Sale Title, Date/Time/Location, and link to Auction Results. If save_csv
        is True (defaut = True) then save the results as a csv file.

        ----------
        Parameters
        ----------
        url             :   string, website url to scrape.
        save_results    :   Boolean, default is true and saves the results as a CSV, if False
                            return the list of results instead of saving to file.
        f_name          :   string, file name to save results as, default is None.

        return          :   list of lists, holds results of scrape [title, date/time, link] 
        """
        self.driver.get(url)

        try:

            site = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "main-list-backbone"))
            )

            self.scroll_to_bottom()

            auction_info = []


            sales = site.find_elements_by_tag_name("li")
            for sale in sales:
                auctions = sale.find_elements_by_class_name("content-body")
                for auction in auctions:

                    try:
                        title = auction.find_element_by_tag_name("h2").text
                    except NoSuchElementException:
                        title = " "
                        
                    try:
                        auction_date = auction.find_element_by_tag_name("p").text
                    except NoSuchElementException:
                        auction_date = " "

                    try:
                        link_element = auction.find_element_by_tag_name("a")
                        link = link_element.get_attribute("href")
                    except NoSuchElementException:
                        link = " "

                    info = [title, auction_date, link]
                    auction_info.append(info)

        finally:
            self.driver.quit()

        self.driver.quit()

        if save_results:
            self.save_to_csv(auction_info, f_name)
        else:
            return auction_info

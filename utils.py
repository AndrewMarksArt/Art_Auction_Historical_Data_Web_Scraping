"""
Common fuctions that are frequently needed to close popups,
scroll to load content, save scraped data, etc.
"""

import time
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class WebDriverUtilities():
    """
    Web Driver utility fucntions for that are commonly needed such as,
    closing cookies, scroll to bottom, infinite scroll, etc...
    """
    def __init__(self, driver):
        """
        initialize the web driver utility class using the config.py file to
        get the path to the chrome driver and initialize the driver object
        """
        self.driver = driver


    def wait_for_class(self, class_name, wait_time = 5):
        """
        function to wait for the presence of an element to appear
        """
        try:
            WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                )
        except:
            print(f"couldnt find {class_name}")

    def close_cookies(self):
        """
        When we first open the web browser find and accept cookies button
        """
        # wait 5 seconds or until the accept cookies button appears
        try:

            self.wait_for_class( "alert-button")
            # find the accept cookies button and click accept
            cookies_btn = self.driver.find_element_by_class_name("alert-button")
            cookies_btn.click()

            # let us know if the button was clicked
            print("we accepted cookies and clicked the button")

            # wait for 3 seconds
            time.sleep(3)

        # quit if cookies button not found
        except NoSuchElementException:
            # let us know if we couldn't find the button
            print("couldn't find the button")
            # close the driver
            self.driver.close()


    def infinite_scroll(self):
        """
        keep scrolling down for pages that load data dynamically when you reach the bottom
        of the page.
        """
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def scroll_to_bottom(self):
        """
        scroll to the bottom of the page.
        """
        # scroll to bottom of page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight")


def save_csv_list(save_path, filename, data):
    """
    given a filename and save path, save the provided list (data) as a csv file
    """
    with open(f'{save_path} {filename}', "w", encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])

def get_auction_links(filename, data_path):
    """
    given a file name for a csv file with urls of auction results, return those urls
    """

    # set path to phillips auctions csv file
    file_path = data_path + filename

    # initialize list for auciton urls
    auction_links = []

    # open the file, and save auction links in a list
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for auction_link in reader:
            # each row has title, date/time, url. Append url to list
            auction_links.append(auction_link)

    # return list of auction urls
    return auction_links

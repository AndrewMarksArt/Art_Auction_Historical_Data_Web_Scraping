# imports
import time
import csv

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import config


def get_auction_links(filename):
    """
    given a file name for a csv file with urls of auction results, return those urls
    """

    # set path to phillips auctions csv file
    FILE_PATH = config.CSV_PATH + filename

    # initialize list for auciton urls
    auction_links = []

    # open the file, and save auction links in a list
    with open(FILE_PATH, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            # each row has title, date/time, url. Append url to list
            auction_links.append(row[2])

    # return list of auction urls
    return auction_links


# urls of auctions
list_auctions = get_auction_links('Phillips_Auctions.csv')

# get url list of Phillips auctions
driver = webdriver.Chrome(config.CHROME_PATH)

# go to url at indext [_]
driver.get(list_auctions[0])

# wait 5 seconds or until the accept cookies button appears
try:
    site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-button"))
    )

    # find the accept cookies button and click accept
    cookies_btn = driver.find_element_by_class_name("alert-button")
    cookies_btn.click()

    # let us know if the button was clicked
    print("we accepted cookies and clicked the button")

    # wait for 3 seconds
    time.sleep(3)

    # find the number of auction lots
    try:
        # header for auction results holds number of lots
        auction_header = driver.find_element_by_class_name("page-header")
        # number of lots is in the span tab
        lots = auction_header.find_element_by_tag_name("span").text
        # span tab hold string with '# lots' format
        # split and get first element as an int
        num_lots = int(lots.split()[0])
    except NoSuchElementException:
        print("could not find number of lots")

    # find grid that holds oll the lots
    grid = driver.find_element_by_class_name("standard-grid")
    lots = grid.find_elements_by_tag_name("li")
    
    urls = []

    for lot in lots:
        link_tag = lot.find_element_by_tag_name("a")
        url = link_tag.get_attribute("href")
        urls.append(url)

    for link in urls:
        print(link)

    # lot = driver.find_element_by_class_name("phillips-lot")
    # lot.click()

    # wait for 3 seconds then close the driver
    time.sleep(3)
    driver.close()

# quit if cookies button not found
except NoSuchElementException:
    # let us know if we couldn't find the button
    print("couldn't find the button")
    # close the driver
    driver.close()



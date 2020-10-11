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
    FILE_PATH = config.PHILLIPS + filename

    # initialize list for auciton urls
    auction_links = []

    # open the file, and save auction links in a list
    with open(FILE_PATH, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            # each row has title, date/time, url. Append url to list
            auction_links.append(row)

    # return list of auction urls
    return auction_links


def scroll_to_bottom():
    """
    scroll to bottom of page
    """
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def close_cookies():
    """
    When we first open the web browser find and accept cookies button
    """
    # wait 5 seconds or until the accept cookies button appears
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-button"))
        )

        # find the accept cookies button and click accept
        cookies_btn = driver.find_element_by_class_name("alert-button")
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
        driver.close()



# urls of auctions
list_auctions = get_auction_links('all_sales_auction_list.csv')

# get url list of Phillips auctions
driver = webdriver.Chrome(config.CHROME_PATH)

no_grid = []
different_layout = []

for i in range(len(list_auctions)):
    # go to url at index[i]
    url = list_auctions[i][-1]
    print(url)

    driver.get(url)
    if i == 0:
        close_cookies()
    
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

    try:
        # find the grid that holds all the lots
        grid = driver.find_element_by_class_name("standard-grid")

        try:
            # find each list element that links to each lot with detials
            lots = grid.find_elements_by_tag_name("li")

            if len(lots) < num_lots:
                scroll_to_bottom()

                print('Scrolling')

                # wait
                time.sleep(2)

                # find the grid that holds all the lots
                grid = driver.find_element_by_class_name("standard-grid")
                # find each list element that links to each lot with detials
                lots = grid.find_elements_by_tag_name("li")

            # initialize an empty list that will hold urls to the lot details
            urls = []

            # loop through the list elements of lots to find the links to all
            # of the lot details
            for lot in lots:
                link_tag = lot.find_element_by_tag_name("a")
                url = link_tag.get_attribute("href")
                urls.append(url)

            with open(f'{config.PHILLIPS_LOTS_CSV} {list_auctions[i][0]} {list_auctions[i][1]}_{str(i)}', "w", encoding='UTF-8', newline='') as f:
                    writer = csv.writer(f)
                    for row in urls:
                        writer.writerow([row])

        except:
            print("Found Grid but no list of results")
            no_grid.append(f'{list_auctions[i][0]} {list_auctions[i][1]}_{i}')

    except:
        print("Different auction results layout -- no grid and no results")
        different_layout.append(f'{list_auctions[i][0]} {list_auctions[i][1]}_{i}')

    # wait for 3 seconds
        time.sleep(3)

# close the driver
driver.close()

with open(f'{config.PHILLIPS_LOTS_CSV} no_gird', "w", encoding='UTF-8', newline='') as f:
    writer = csv.writer(f)
    for row in no_grid:
        writer.writerow([row])


with open(f'{config.PHILLIPS_LOTS_CSV} different_layout', "w", encoding='UTF-8', newline='') as f:
    writer = csv.writer(f)
    for row in different_layout:
        writer.writerow([row])

"""
load list of auctions to scrape, loop through each auction, try to find links to each
lot item, then save list of lot items to disk.
"""

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import config
import utils


# urls of auctions
list_of_auctions = utils.get_auction_links('all_sales_auction_list.csv', config.PHILLIPS)
batch = list_of_auctions[221:]


for idx, auction_info in enumerate(batch):

    # initialize the web driver to open the chrome browser
    driver = webdriver.Chrome(config.CHROME_PATH)

    # use the driver to initialize the utils class for helper functions
    utilities = utils.WebDriverUtilities(driver)

    sale = auction_info[0].replace('/', '').replace('\\', '')
    date_raw = auction_info[1].split()[:3]
    date = "_".join(map(str, date_raw)).replace('/','').replace('\\', '').replace('<', '').replace('>', '').replace('&nbsp',' ').replace(',', '').replace('-',' ')
    url = auction_info[-1]

    # give the url to the driver so it can navigate to the web page
    driver.get(url)

    # close cookies pop up if there
    utilities.close_cookies()

    # find the number of auction lots
    try:
        # wait for element to load
        utilities.wait_for_class("page-header")
        # header for auction results holds number of lots
        auction_header = driver.find_element_by_class_name("page-header")
        # number of lots is in the span tab
        num_lots = auction_header.find_element_by_tag_name("span").text
        # span tab hold string with '# lots' format
        # split and get first element as an int
        num_lots = int(num_lots.split()[0])

    # raise an exception and print out when we cant find the lot numbers
    # add the aution to the cant find lots list, we will save this to file
    # and review auctions where this fails later.
    except NoSuchElementException:
        print(f"could not find number of lots: {idx}")
        # cant_find_num_lots.append(auction)

    # locate all lot items on page
    try:

        # wait for element to load
        utilities.wait_for_class("standard-grid")

        # find the grid that holds all the lots
        grid = driver.find_element_by_class_name("standard-grid")

        # find lot details
        lots = grid.find_elements_by_tag_name("li")

        # wait for 2 seconds
        time.sleep(2)

        # initialize an empty list that will hold urls to the lot details
        urls = []

        # scroll to bottom of page
        utilities.infinite_scroll()

        # wait a few seconds
        time.sleep(2)

        # loop through the list elements of lots to find the links to all
        # of the lot details, each lot is in a <li> tag, links are in <a>
        # and url is "href" attribute of <a> tag
        for lot in lots:
            link_tag = lot.find_element_by_tag_name("a")
            url = link_tag.get_attribute("href")
            # append url to list of lot urls
            urls.append(url)

        # save the list of lot urls to disk
        file_name = f'{idx}_{sale}_{date}_{num_lots}'
        utils.save_csv_list(config.PHILLIPS_LOTS_CSV, file_name, urls)

    except NoSuchElementException:
        print(f"could not locate standard grid at index: {idx}")

    # wait for 10 seconds
    time.sleep(2)

    # close the driver
    driver.close()

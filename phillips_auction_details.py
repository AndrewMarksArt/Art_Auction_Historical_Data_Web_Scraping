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
list_auctions = utils.get_auction_links('all_sales_auction_list.csv', config.PHILLIPS)

# initialize the web driver to open the chrome browser
driver = webdriver.Chrome(config.CHROME_PATH)

# use the driver to initialize the utils class for helper functions
utilities = utils.WebDriverUtilities(driver)

# set up lists to hold auction names where there were issues
grid_no_lots = []
different_layout = []
cant_find_num_lots = []

# loop over list of auctions
for i in range(len(list_auctions)):
    # go to url at index[i][-1], each list_auction tuple is made up of
    # the auction title, the date and location, and the link. [-1] makes
    # sure we get the link since it is the last element of the tuple
    auction = list_auctions[i]
    url = auction[-1]

    # give the url to the driver so it can navigate to the web page
    driver.get(url)

    # for the first url we need to click the accept cookies btn
    if i == 0:
        utilities.close_cookies()
    
    # find the number of auction lots
    try:
        # wait for element to load
        utilities.wait_for_class("page-header")
        # header for auction results holds number of lots
        auction_header = driver.find_element_by_class_name("page-header")
        # number of lots is in the span tab
        lots = auction_header.find_element_by_tag_name("span").text
        # span tab hold string with '# lots' format
        # split and get first element as an int
        num_lots = int(lots.split()[0])

    # raise an exception and print out when we cant find the lot numbers
    # add the aution to the cant find lots list, we will save this to file
    # and review auctions where this fails later.
    except NoSuchElementException:
        print("could not find number of lots")
        cant_find_num_lots.append(auction)

    # locate all lot items on page
    try:

        # wait for element to load
        utilities.wait_for_class("standard-grid")

        # find the grid that holds all the lots
        grid = driver.find_element_by_class_name("standard-grid")

        # wait for 2 seconds
        time.sleep(2)

        try:
            # find each list element that links to each lot with detials
            lots = grid.find_elements_by_tag_name("li")
            for lot in lots:
                temp = lot.find_element_by_tag_name("a")
                url = link_tag.get_attribute("href")
                print(url)

            # check to see if all lots have loaded or if we need to scroll
            # to the bottom of the page to load everything
            if len(lots) < num_lots:
                utilities.scroll_to_bottom()

                # wait
                time.sleep(2)

                # find the grid that holds all the lots
                grid = driver.find_element_by_class_name("standard-grid")
                # find each list element that links to each lot with detials
                lots = grid.find_elements_by_tag_name("li")

            # initialize an empty list that will hold urls to the lot details
            urls = []

            # loop through the list elements of lots to find the links to all
            # of the lot details, each lot is in a <li> tag, links are in <a>
            # and url is "href" attribute of <a> tag
            for lot in lots:
                link_tag = lot.find_element_by_tag_name("a")
                url = link_tag.get_attribute("href")
                # append url to list of lot urls
                urls.append(url)
                print(url)

            # save the list of lot urls to disk
            file_name = f'{auction[0]} {auction[1]}_{str(i)}'
            utils.save_csv_list(config.PHILLIPS_LOTS_CSV, file_name, urls)

        # raise an exception if we found the grid class but couldn't find the lots
        except NoSuchElementException:
            # print out that we found grid but no lots with aution title
            # and date/time/location
            print("\nFound Grid but no list of results")
            print(f'{auction[0], auction[1]}')
            # append auction tuple information to be saved
            grid_no_lots.append(auction)

    # raise exception that we couldn't find the grid layout
    except:
        # print that we couldn't find the grid layout with aution details
        print("\nDifferent auction results layout -- no grid and no results")
        print(f'{auction[0], auction[1]}')
        # save auction tuple information to be saved
        different_layout.append(auction)

    # wait for 10 seconds
        time.sleep(10)

# close the driver
driver.close()

utils.save_csv_list("grid_no_lots", config.PHILLIPS_LOTS_CSV, grid_no_lots)
utils.save_csv_list("dif_layout", config.PHILLIPS_LOTS_CSV, different_layout)
utils.save_csv_list("cant_find_num_lots", config.PHILLIPS_LOTS_CSV, cant_find_num_lots)


import time
import csv

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


    def scroll_to_bottom(self, min_wait=5, max_wait=15, scroll_speed=10):
        """
        For pages that load content dynamically as the user scrolls this allows us to
        scroll down to the bottom of the page so we can let the content we need load.

        ----------
        Parameters
        ----------
        min_wait        :   int, min wait time for the randint function
        max_wait        :   int, max wait time for the randint function
        scroll_speed    :   int, larger for faster speed
        """

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # calculate where we are on page, try to scroll down, re-calculate
        # where we are on the page. If the page hasn't scrolled down we are
        # at the bottom of the page and break out of the loop.
        while True:
            # set a random wait time for each loop between 5 and 15 seconds
            wait = randint(min_wait, max_wait)

            # Scroll down to bottom
            for i in range(1, last_height, scroll_speed):
                self.driver.execute_script(f"window.scrollTo(0, {last_height});")

            # Wait to load page randomly between 1 and 10 seconds
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
        with open(f_name, "w", encoding='UTF-8', newline='') as f:
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
        # use the chrome driver to navigate to the provided url
        self.driver.get(url)

        # using try / finally, we want to wait for the content to load
        # if the content doesn't load after the wait time we will close the driver
        try:
            # wait 5 seconds or until the content we are looking for loads
            site = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "main-list-backbone"))
            )

            # site loads results dynamically as we scroll so scroll to bottom of page
            self.scroll_to_bottom()

            # initialize list that will hold results
            auction_info = []

            # find list items from the section we are interested in and create
            # a list of elements with the HTML tag we are looking for
            sales = site.find_elements_by_tag_name("li")

            # loop through the list items we have scraped
            for sale in sales:
                # find the content we need from the list items
                auctions = sale.find_elements_by_class_name("content-body")
                
                # loop through the list of specific content
                for auction in auctions:

                    # look for auction title, if not there set to " "
                    try:
                        title = auction.find_element_by_tag_name("h2").text
                    except NoSuchElementException:
                        title = " "
                        
                    # look for the date/time/location of the auction or set to " "
                    try:
                        auction_date = auction.find_element_by_tag_name("p").text
                    except NoSuchElementException:
                        auction_date = " "

                    # look for the link to the auction results or set to " "
                    try:
                        link_element = auction.find_element_by_tag_name("a")
                        link = link_element.get_attribute("href")
                    except NoSuchElementException:
                        link = " "

                    # create a temp list with information for this auction
                    temp = [title, auction_date, link]

                    # append the temp list with current information to all auction
                    # information list that holds all resutls
                    auction_info.append(temp)

            # close the driver once we have the information we need
            self.driver.quit()

        # if try fails -> content doesn't load by the end o four wait time close the driver
        finally:
            self.driver.quit()

        # if save results is True save auction data to csv file
        if save_results:
            self.save_to_csv(auction_info, f_name)

        # if save results is False return the aution data
        else:
            return auction_info



    def sothebys(self, url, save_results=True, f_name=None):
        """
        Get Sothebys data
        """
        # use the chrome driver to navigate to the provided url
        self.driver.get(url)

        # using try / finally, we want to wait for the content to load
        # if the content doesn't load after the wait time we will close the driver
        try:
            # wait 5 seconds or until the content we are looking for loads
            site = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "searchModule"))
            )

            # site loads results dynamically as we scroll so scroll to bottom of page
            self.scroll_to_bottom()

            # initialize list that will hold results
            auction_info = []
            
            # find list items from the section we are interested in and create
            # a list of elements with the HTML tag we are looking for
            sales = site.find_elements_by_tag_name("li")

            # loop through the list items we have scraped
            for sale in sales:
                # find the content we need from the list items
                auctions = sale.find_elements_by_class_name("Card-info")
                
                # loop through the list of specific content
                for auction in auctions:

                    # look for auction title, if not there set to " "
                    try:
                        title = auction.find_element_by_class_name("Card-title").text
                    except NoSuchElementException:
                        title = " "
                        
                    # look for the date/time/location of the auction or set to " "
                    try:
                        auction_date = auction.find_element_by_class_name("Card-details").text
                    except NoSuchElementException:
                        auction_date = " "

                    # look for the link to the auction results or set to " "
                    try:
                        link_element = auction.find_element_by_tag_name("a")
                        link = link_element.get_attribute("href")
                    except NoSuchElementException:
                        link = " "

                    # create a temp list with information for this auction
                    temp = [title, auction_date, link]

                    # append the temp list with current information to all auction
                    # information list that holds all resutls
                    auction_info.append(temp)
                    
            # close the driver once we have the information we need
            self.driver.quit()

        # if try fails -> content doesn't load by the end o four wait time close the driver
        finally:
            self.driver.quit()

        # if save results is True save auction data to csv file
        if save_results:
            self.save_to_csv(auction_info, f_name)

        # if save results is False return the aution data
        else:
            return auction_info


    def christies(self, url):
        """

        """
        # use the chrome driver to navigate to the provided url
        self.driver.get(url)
        time.sleep(5)
        allow_cookies = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[4]/div[2]/div/button')
        allow_cookies.click()
        body = self.driver.find_element_by_css_selector('body')

        xpath = '/html/body/main/div[3]/section/div/chr-calendar/div/section[2]/chr-calendar-list/section/footer/chr-pagination/chr-button[1]/a'

        auction_details = []
        counter = 0
        while counter < 241:
            temp = self.get_christies_details()
            body.send_keys(Keys.PAGE_UP)
            time.sleep(1)
            try:
                self.scroll_to_bottom(min_wait=1, max_wait=2, scroll_speed=10)
                body.send_keys(Keys.PAGE_UP)
                site = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/section/div/chr-calendar/div/section[2]/chr-calendar-list/section/footer/chr-pagination/chr-button/a')))
                button = self.driver.find_element_by_xpath(xpath)
                time.sleep(3)
                button.click()
            except NoSuchElementException:
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(3)
                body.send_keys(Keys.PAGE_UP)
                site = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, xpath)))
                button = self.driver.find_element_by_xpath(xpath)
                time.sleep(3)
                button.click()

        
            auction_details.append(temp)
            
            counter += 1
            print(counter)

        self.driver.quit()

        with open('christies_test', "w", encoding='UTF-8', newline='') as f:
            writer = csv.writer(f)
            for row in auction_details:
                for sale in row:
                    writer.writerow(sale)



    def get_christies_details(self):
        """

        """

        # initialize list that will hold results
        auction_info = []

        # using try / finally, we want to wait for the content to load
        # if the content doesn't load after the wait time we will close the driver
        try:
            # wait 5 seconds or until the content we are looking for loads
            site = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.ID, "calendar-tab"))
            )

            # site loads results dynamically as we scroll so scroll to bottom of page
            self.scroll_to_bottom(min_wait=1, max_wait=2, scroll_speed=20)
            
            # find list items from the section we are interested in and create
            # a list of elements with the HTML tag we are looking for
            sales = site.find_elements_by_tag_name("li")

            # loop through the list items we have scraped
            for sale in sales:
                # find the content we need from the list items
                auctions = sale.find_elements_by_class_name("container-fluid")
                
                # loop through the list of specific content
                for auction in auctions:

                    # look for auction title, if not there set to " "
                    try:
                        title = auction.find_element_by_tag_name("h4").text
                    except NoSuchElementException:
                        title = " "
                        
                    # look for the date/time/location of the auction or set to " "
                    try:
                        date = auction.find_element_by_xpath("/html/body/main/div[3]/section/div/chr-calendar/div/section[2]/chr-calendar-list/section/chr-events-range/chr-viz-sensor/div/ul/li[1]/chr-event-tile/section/div[1]/span/span[2]").text
                        location = auction.find_element_by_xpath("/html/body/main/div[3]/section/div/chr-calendar/div/section[2]/chr-calendar-list/section/chr-events-range/chr-viz-sensor/div/ul/li[1]/chr-event-tile/section/div[2]/div[2]/span").text
                        auction_date = (date + ' ' + location).replace('\n', ' ')
                    except NoSuchElementException:
                        auction_date = " "

                    # look for the link to the auction results or set to " "
                    try:
                        link_element = auction.find_element_by_tag_name("a")
                        link = link_element.get_attribute("href")
                    except NoSuchElementException:
                        link = " "

                    # create a temp list with information for this auction
                    temp = [title, auction_date, link]

                    # append the temp list with current information to all auction
                    # information list that holds all resutls
                    auction_info.append(temp)
                    
            # close the driver once we have the information we need
            #self.driver.quit()

        except:
            pass

        return auction_info



sothebys = 'https://www.sothebys.com/en/results?from=&to=&f2=00000164-609b-d1db-a5e6-e9ff01230000&f2=00000164-609b-d1db-a5e6-e9ff08ab0000&f3=LIVE&f3=ONLINE&q='
christies = 'https://www.christies.com/en/results?filters=|category_7|'
chrome_path = r'C:\Program Files (x86)\chromedriver.exe'

test = HistoricalAuctionRecords(chrome_path)

#test.sothebys(sothebys, save_results=True, f_name='Sothebys_Auctions.csv')

test.christies(christies)



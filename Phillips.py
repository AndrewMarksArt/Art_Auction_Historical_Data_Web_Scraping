import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://www.phillips.com/auctions/past/filter/Department%3DContemporary/sort/oldest")

time.sleep(5)

try:
    print('waiting for site to load')

    site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "main-list-backbone"))
    )

    print('start scrolling')

    # scroll wait time
    wait = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(wait)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    auction_info = []

    print('getting auction Titles, Sale date/time, and Link to sale')

    sales = site.find_elements_by_tag_name("li")
    for sale in sales:
        auctions = sale.find_elements_by_class_name("content-body")
        for auction in auctions:

            title = auction.find_element_by_tag_name("h2").text
           
            try:
                auction_date = auction.find_element_by_tag_name("p").text
            except:
                auction_date = " "

            link = auction.find_element_by_tag_name("a")
            info = [title, auction_date, link.get_attribute("href")]
            auction_info.append(info)
        

finally:
    driver.quit()

print('close window')

driver.quit()

print('writing auction information to csv file')

with open("Phillips_Auctions.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for row in auction_info:
        writer.writerow(row)

print('finished')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://www.phillips.com/auctions/past/filter/Department%3DContemporary/sort/oldest")

time.sleep(5)

try:
    main = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/ul/li[1]/div[1]/a'))
    )
except:
    driver.quit()

element = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/ul/li[1]/div[1]/a')
auction_link = element.get_attribute('href')
print(f'This is the link to the oldest auction available: {auction_link}')

driver.quit()

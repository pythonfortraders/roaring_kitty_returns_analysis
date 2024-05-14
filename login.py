from selenium import webdriver

import pickle
import time

driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

time.sleep(15)

cookies = driver.get_cookies()
with open("twitter_cookies.pkl", "wb") as file:
    pickle.dump(cookies, file)

driver.quit()

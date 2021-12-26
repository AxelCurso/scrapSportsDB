from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_class(d, c):
    try:
        d.find_element_by_class_name(c)
    except NoSuchElementException:
        return False
    return True

def getBase(pre, post, y):
    base = pre + str(y) + "-" + str(int(y)+1) + post
    return base

def getDatabase(url):
    allUrls = []
    driver = webdriver.Chrome()
    driver.get(url)
    while (check_exists_by_class(driver, "event__more")):
        next = driver.find_element_by_class_name("event__more")
        actions = ActionChains(driver);
        actions.click(next).perform();
    links = driver.find_elements_by_class_name("event__match")
    print(len(links))
    driver.close()

prebase = "https://www.flashscore.fr/football/france/ligue-1-"
postbase = "/resultats/"
year = date.today().strftime("%Y")
# for i in range(10):
for i in range(1):
    base = getBase(prebase, postbase, int(year)-i)
    print("Getting data for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    getDatabase(base)

# base = getBase(prebase, postbase)
# print(base)
# s = pd.Series([1, 3, 5, np.nan, 6, 8], [1, 3, 5, np.nan, 6, 8])
# print(s)
# driver = webdriver.Chrome()

import sys
import datetime
from time import sleep
from progress.bar import ShadyBar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_class(d, c):
    try:
        d.find_element_by_class_name(c)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_id(d, c):
    try:
        d.find_element_by_id(c)
    except NoSuchElementException:
        return False
    return True

def getMatchsLinks(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    links = []
    if (check_exists_by_id(driver, "onetrust-accept-btn-handler")):
        sleep(0.2)
        action = ActionChains(driver)
        action.click(driver.find_element_by_id("onetrust-accept-btn-handler")).perform()
    if (check_exists_by_class(driver, "ab-in-app-message")):
        action = ActionChains(driver)
        action.click(driver.find_element_by_class_name("ab-close-button")).perform()
    # while (check_exists_by_class(driver, "ab-in-app-message") == False):
    #     continue
    # action = ActionChains(driver)
    # action.click(driver.find_element_by_class_name("ab-close-button")).perform()
    a_s = driver.find_elements_by_tag_name("a")
    for a in a_s:
        if (a.get_attribute("data-text") == "GAME DETAILS"):
            links.append(a.get_attribute("href"))
    driver.close()
    return links

# "https://www.nba.com/games?date=2022-01-26"
if (len(sys.argv) != 2):
    print("USAGE: python3 get_raw_matchs.py $YEAR")
    exit()
url = "https://www.nba.com/games?date="
year = int(sys.argv[1])
d1 = datetime.date(year, 1, 1)
d2 = datetime.date(year, 12, 31)
days = [d1 + datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]
matchsLinks = []
bar = ShadyBar("  - Getting all the matchs' links for the year "+str(year), max=len(days), suffix="%(index)d/%(max)d | %(percent)d%% => %(elapsed)dsec. | ETA: %(eta)dsec.")
for day in days[:2]:
    matchsLinks += getMatchsLinks(url+str(day))
    bar.next()
bar.finish()
output_file = open('matchs_links.txt', 'w')
for link in matchsLinks:
    output_file.write(link+'\n')
output_file.close()
print("    -> Data saved at ./matchs_links.txt")

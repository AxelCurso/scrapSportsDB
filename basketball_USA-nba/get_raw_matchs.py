import sys
import os
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

def getMatchStats(url, id):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    stats = []
    count = 0
    if (check_exists_by_id(driver, "onetrust-accept-btn-handler")):
        sleep(0.2)
        action = ActionChains(driver)
        action.click(driver.find_element_by_id("onetrust-accept-btn-handler")).perform()
    while (check_exists_by_class(driver, "ab-in-app-message") == False and count < 10):
        sleep(0.1)
        count += 1
    if (check_exists_by_class(driver, "ab-in-app-message")):
        action = ActionChains(driver)
        action.click(driver.find_element_by_class_name("ab-close-button")).perform()
    box = driver.find_element_by_class_name("Block_blockContainer__2tJ58")
    boxTables = box.find_elements_by_class_name("GameLinescore_table__1AeWc")
    box1stpart = boxTables[0].find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    box2ndpart = boxTables[1].find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    box3rdpart = box.find_element_by_class_name("GameLinescore_boxes__3d94c").find_elements_by_tag_name("div")
    # INFOS
    stats.append(id)
    stats.append(box.find_element_by_class_name("BlockTitle_base__1s_ij").find_element_by_tag_name("span").get_attribute("innerHTML"))
    stats.append(box1stpart[1].find_element_by_tag_name("span").get_attribute("innerHTML"))
    stats.append(box1stpart[0].find_element_by_tag_name("span").get_attribute("innerHTML"))
    stats.append(int(box1stpart[1].find_elements_by_tag_name("td")[-1].get_attribute("innerHTML")))
    stats.append(int(box1stpart[0].find_elements_by_tag_name("td")[-1].get_attribute("innerHTML")))
    stats.append(int(box3rdpart[0].find_elements_by_tag_name("p")[-1].get_attribute("innerHTML")))
    stats.append(int(box3rdpart[1].find_elements_by_tag_name("p")[-1].get_attribute("innerHTML")))
    # SUMMARY
    hb1tds = box1stpart[1].find_elements_by_tag_name("td")
    ab1tds = box1stpart[0].find_elements_by_tag_name("td")
    stats.append(int(hb1tds[1].get_attribute("innerHTML")))
    stats.append(int(hb1tds[2].get_attribute("innerHTML")))
    stats.append(int(hb1tds[3].get_attribute("innerHTML")))
    stats.append(int(hb1tds[4].get_attribute("innerHTML")))
    stats.append(int(ab1tds[1].get_attribute("innerHTML")))
    stats.append(int(ab1tds[2].get_attribute("innerHTML")))
    stats.append(int(ab1tds[3].get_attribute("innerHTML")))
    stats.append(int(ab1tds[4].get_attribute("innerHTML")))
    stats += [int(k.get_attribute("innerHTML")) for k in box2ndpart[1].find_elements_by_tag_name("td")]
    stats += [int(k.get_attribute("innerHTML")) for k in box2ndpart[0].find_elements_by_tag_name("td")]
    # TRADITIONAL
    # /box-score?type=traditional
    # HUSTLE
    print(stats)
    while (1):
        continue
    driver.close()
    return stats

if (len(sys.argv) != 2):
    print("USAGE: python3 get_raw_matchs.py $YEAR")
    exit()
year = int(sys.argv[1])
if not os.path.exists("./"+str(year)+"/sample_matchs_links.txt"):
    print("ERROR: no file containing the links for the year "+str(year))
input_file = open("./"+str(year)+"/sample_matchs_links.txt", 'r')
lines = input_file.readlines()
input_file.close()
links = []
for line in lines:
    links.append(line.strip())
datas = []
bar = ShadyBar("  - Getting all the matchs' stats for the year "+str(year), max=len(links), suffix="%(index)d/%(max)d | %(percent)d%% => %(elapsed)dsec. | ETA: %(eta)dsec.")
for i in range(len(links[:2])):
    datas.append(getMatchStats(links[i], int(str(year)+"{:05d}".format(i))))
    bar.next()
bar.finish()
print(datas)

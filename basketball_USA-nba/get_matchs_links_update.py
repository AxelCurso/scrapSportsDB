import sys
import datetime
import pandas as pd
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


def check_exists_by_tag(d, c):
    try:
        d.find_element_by_tag_name(c)
    except NoSuchElementException:
        return False
    return True

def getMatchStats(url, id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="/home/axel/chromedriver", options=chrome_options)
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
    driver.get(url + "/box-score?type=traditional")
    tables = driver.find_elements_by_class_name("StatsTable_table__2gqz8")
    rows = [k.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[-1].find_elements_by_tag_name("td") for k in tables]
    homeElems = []
    for elem in rows[1]:
        if (check_exists_by_tag(elem, "a")):
            homeElems.append(elem.find_element_by_tag_name("a").get_attribute("innerHTML"))
        else:
            homeElems.append(elem.get_attribute("innerHTML"))
    awayElems = []
    for elem in rows[0]:
        if (check_exists_by_tag(elem, "a")):
            awayElems.append(elem.find_element_by_tag_name("a").get_attribute("innerHTML"))
        else:
            awayElems.append(elem.get_attribute("innerHTML"))
    stats.append(int(homeElems[3]))
    stats.append(float(homeElems[4]))
    stats.append(int(homeElems[6]))
    stats.append(float(homeElems[7]))
    stats.append(int(homeElems[9]))
    stats.append(float(homeElems[10]))
    stats.append(int(homeElems[11]))
    stats.append(int(homeElems[12]))
    stats.append(int(homeElems[14]))
    stats.append(int(homeElems[15]))
    stats.append(int(homeElems[16]))
    stats.append(int(homeElems[17]))
    stats.append(int(homeElems[18]))
    stats.append(int(awayElems[3]))
    stats.append(float(awayElems[4]))
    stats.append(int(awayElems[6]))
    stats.append(float(awayElems[7]))
    stats.append(int(awayElems[9]))
    stats.append(float(awayElems[10]))
    stats.append(int(awayElems[11]))
    stats.append(int(awayElems[12]))
    stats.append(int(awayElems[14]))
    stats.append(int(awayElems[15]))
    stats.append(int(awayElems[16]))
    stats.append(int(awayElems[17]))
    stats.append(int(awayElems[18]))
    # HUSTLE
    driver.get(url + "/box-score?type=hustle")
    tables = driver.find_elements_by_class_name("StatsTable_table__2gqz8")
    rows = [k.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[-1].find_elements_by_tag_name("td") for k in tables]
    homeElems = []
    for elem in rows[1]:
        if (check_exists_by_tag(elem, "a")):
            homeElems.append(elem.find_element_by_tag_name("a").get_attribute("innerHTML"))
        else:
            homeElems.append(elem.get_attribute("innerHTML"))
    awayElems = []
    for elem in rows[0]:
        if (check_exists_by_tag(elem, "a")):
            awayElems.append(elem.find_element_by_tag_name("a").get_attribute("innerHTML"))
        else:
            awayElems.append(elem.get_attribute("innerHTML"))
    stats.append(int(homeElems[2]))
    stats.append(int(homeElems[3]))
    stats.append(int(homeElems[4]))
    stats.append(int(homeElems[5]))
    stats.append(int(homeElems[6]))
    stats.append(int(homeElems[9]))
    stats.append(int(homeElems[10]))
    stats.append(int(homeElems[12]))
    stats.append(int(homeElems[13]))
    stats.append(int(awayElems[2]))
    stats.append(int(awayElems[3]))
    stats.append(int(awayElems[4]))
    stats.append(int(awayElems[5]))
    stats.append(int(awayElems[6]))
    stats.append(int(awayElems[9]))
    stats.append(int(awayElems[10]))
    stats.append(int(awayElems[12]))
    stats.append(int(awayElems[13]))
    # print(stats)
    # while (1):
    #     continue
    driver.close()
    return stats

def getMatchsLinks(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    links = []
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

url = "https://www.nba.com/games?date="
last_update = open("./last_update.txt", "r")
today = datetime.date.today()
previous = datetime.date.fromisoformat(last_update.readline().strip())
last_update.close()
days = [previous + datetime.timedelta(days=x) for x in range((today-previous).days+1)]
matchsLinks = []
bar = ShadyBar("  - Getting all the matchs' links from "+str(days[0])+" to "+str(days[-1]), max=len(days), suffix="%(index)d/%(max)d | %(percent)d%% => %(elapsed)dsec. | ETA: %(eta)dsec.")
for day in days:
    matchsLinks += getMatchsLinks(url+str(day))
    bar.next()
bar.finish()
header =    [
            "id", "date", "homeTeam", "awayTeam", "h_score", "a_score", "lc", "tc",
            "h_q1", "h_q2", "h_q3", "h_q4", "h_pitp", "h_fbpts", "h_bigld", "h_benchpts", "h_tmreb", "h_tov", "h_tmtov", "h_ptsofto",
            "a_q1", "a_q2", "a_q3", "a_q4", "a_pitp", "a_fbpts", "a_bigld", "a_benchpts", "a_tmreb", "a_tov", "a_tmtov", "a_ptsofto",
            "h_fga", "h_fgp", "h_3pa", "h_3pp", "h_fta", "h_ftp", "h_oreb", "h_dreb", "h_ast", "h_stl", "h_blk", "h_to", "h_pf",
            "a_fga", "a_fgp", "a_3pa", "a_3pp", "a_fta", "a_ftp", "a_oreb", "a_dreb", "a_ast", "a_stl", "a_blk", "a_to", "a_pf",
            "h_sa", "h_sap", "h_dfl", "h_olbr", "h_dlbr", "h_c2s", "h_c3s", "h_obo", "h_dbo",
            "a_sa", "a_sap", "a_dfl", "a_olbr", "a_dlbr", "a_c2s", "a_c3s", "a_obo", "a_dbo"
            ]
datas = []
bar = ShadyBar("  - Getting all the matchs' stats from "+str(days[0])+" to "+str(days[-1]), max=len(matchsLinks), suffix="%(index)d/%(max)d | %(percent)d%% => %(elapsed)dsec. | ETA: %(eta)dsec.")
for i in range(len(matchsLinks)):
    datas.append(getMatchStats(matchsLinks[i], int(str(today.year)+"{:05d}".format(i))))
    bar.next()
bar.finish()
pd.DataFrame(datas).to_csv(+"./tmp_raw_matchs.csv", header=header, index=None)
print("   Data saved: ./tmp_raw_matchs.csv")
print()
last_update = open("./last_update.txt", "w")
last_update.write(str(today))
last_update.close()

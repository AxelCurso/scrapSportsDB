import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
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

def getMatchDatas(match, index):
    url = "https://www.flashscore.fr/match/" + match + "/#resume-du-match/statistiques-du-match"
    # driver = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    driver.get(url)
    while (check_exists_by_class(driver, "has-reject-all-button") == False):
        continue
    ActionChains(driver).click(driver.find_element_by_id("onetrust-reject-all-handler")).perform()
    nameToID = pd.read_csv("./NameToID.csv")
    datas = []
    #id
    datas.append(index+1)
    #date and hour
    matchTime = driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[1]/div").get_attribute('innerHTML').split(' ')
    date = matchTime[0].split('.')
    hour = matchTime[1].split(':')
    datas.append(int(str(date[2]) + str(date[1]) + str(date[0])))
    datas.append(int(str(hour[0]) + str(hour[1])))
    #matchLeagueNb
    nb = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/span[3]/a").get_attribute('innerHTML').split(' ')[-1]
    if (nb.isdigit()):
        datas.append(nb)
    else:
        datas.append(-1)
    #team A and B
    home = driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[2]/div[4]/div[2]/a").get_attribute('innerHTML')
    datas.append(nameToID[nameToID['flashscoreName'] == home].iloc[0]['id'])
    datas.append(nameToID[nameToID['flashscoreName'] == home].iloc[0]['abbr'])
    away = driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[4]/div[4]/div[1]/a").get_attribute('innerHTML')
    datas.append(nameToID[nameToID['flashscoreName'] == away].iloc[0]['id'])
    datas.append(nameToID[nameToID['flashscoreName'] == away].iloc[0]['abbr'])
    #score
    datas.append(driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[3]/div/div[1]/span[1]").get_attribute('innerHTML'))
    datas.append(driver.find_element_by_xpath("/html/body/div[2]/div/div[4]/div[3]/div/div[1]/span[3]").get_attribute('innerHTML'))
    #HOME STATS
    homeStats = driver.find_elements_by_class_name("statHomeValue")
    #AWAY STATS
    awayStat = driver.find_elements_by_class_name("statAwayValue")
    if (len(homeStats) == 17):
        for i in range(len(homeStats)):
            if (i == 11):
                datas.append(0)
            if (i == 0):
                datas.append(int(homeStats[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(homeStats[i].get_attribute('innerHTML')))
        for i in range(len(awayStat)):
            if (i == 11):
                datas.append(0)
            if (i == 0):
                datas.append(int(awayStat[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(awayStat[i].get_attribute('innerHTML')))
    elif (len(homeStats) == 16):
        for i in range(len(homeStats)):
            if (i == 11):
                datas.append(0)
                datas.append(0)
            if (i == 0):
                datas.append(int(homeStats[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(homeStats[i].get_attribute('innerHTML')))
        for i in range(len(awayStat)):
            if (i == 11):
                datas.append(0)
                datas.append(0)
            if (i == 0):
                datas.append(int(awayStat[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(awayStat[i].get_attribute('innerHTML')))
    elif (len(homeStats) == 18):
        for i in range(len(homeStats)):
            if (i == 0):
                datas.append(int(homeStats[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(homeStats[i].get_attribute('innerHTML')))
        for i in range(len(awayStat)):
            if (i == 0):
                datas.append(int(awayStat[i].get_attribute('innerHTML').split('%')[0]))
            else:
                datas.append(int(awayStat[i].get_attribute('innerHTML')))
    else:
        for i in range(34):
            datas.append(-1)
    driver.close()
    return datas

def getDatabase(url):
    datas = []
    # driver = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    driver.get(url)
    while (check_exists_by_class(driver, "has-reject-all-button") == False):
        continue
    ActionChains(driver).click(driver.find_element_by_id("onetrust-reject-all-handler")).perform()
    while (check_exists_by_class(driver, "event__more")):
        next = driver.find_element_by_class_name("event__more")
        actions = ActionChains(driver);
        desired_y = (next.size['height'] / 2) + next.location['y']
        current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        # actions.scroll_into_view(next).perform();
        actions.click(next).perform();
        time.sleep(0.5)
    links = driver.find_elements_by_class_name("event__match")
    print("   Found: " + str(len(links)) + " matchs.")
    matchsIds = [(link.get_attribute('id').split('_')[2]) for link in links]
    driver.close()
    # for i in range(len(matchsIds)):
    #     datas.append(getMatchDatas(matchsIds[i], i))
    columnsName = ["id", "date", "hour", "leagueMatchNb", "idHome", "homeTeam", "idAway", "awayTeam", "h_score", "a_score", "h_possession", "h_shots", "h_targettedShots", "h_nonTargettedShots", "h_blockedShots", "h_freeKicks", "h_corners", "h_offPlays", "h_throwsIns", "h_goalKeeperSaves", "h_fouls", "h_redCards", "h_yellowCards", "h_attemptedPasses", "h_succeededPasses", "h_tackles", "h_attacks", "h_dangerousAttacks", "a_possession", "a_shots", "a_targettedShots", "a_nonTargettedShots", "a_blockedShots", "a_freeKicks", "a_corners", "a_offPlays", "a_throwsIns", "a_goalKeeperSaves", "a_fouls", "a_redCards", "a_yellowCards", "a_attemptedPasses", "a_succeededPasses", "a_tackles", "a_attacks", "a_dangerousAttacks"]
    datas.append(columnsName)
    printProgressBar(0, len(matchsIds), prefix="   Progress:", suffix="Complete (0/"+str(len(matchsIds))+")")
    for i in range(len(matchsIds)):
        datas.append(getMatchDatas(matchsIds[i], i))
        printProgressBar(i+1, len(matchsIds), prefix="   Progress:", suffix="Complete ("+str(i+1)+"/"+str(len(matchsIds))+")")
    # datas.append(getMatchDatas(matchsIds[0], 0))
    # print(datas)
    return datas

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

# MAIN
prebase = "https://www.flashscore.fr/football/france/ligue-1-"
postbase = "/resultats/"
# year = date.today().strftime("%Y")
if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
# for i in range(10):
for i in range(nbYearToGet):
    base = getBase(prebase, postbase, int(year)-i)
    print("Getting data for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    csvDatas = np.asarray(getDatabase(base))
    # print(csvDatas)
    try:
        os.makedirs(str(int(year)-i)+"-"+str(int(year)-i+1))
    except FileExistsError:
        pass
    pd.DataFrame(csvDatas).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/Match.csv", header=None, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/Match.csv\n")

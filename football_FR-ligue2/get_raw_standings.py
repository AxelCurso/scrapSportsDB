import os
import sys
import time
from datetime import date
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

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

def check_exists_by_class(d, c):
    try:
        d.find_element_by_class_name(c)
    except NoSuchElementException:
        return False
    return True

def getLeaderboard(url):
    leaderboard = []
    leaderboard.append(int(url.split('=')[-1]))
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "didomi-continue-without-agreeing")):
        continueWithoutAgreeing = driver.find_element_by_class_name("didomi-continue-without-agreeing")
        actions = ActionChains(driver)
        actions.click(continueWithoutAgreeing).perform()
    table = driver.find_elements_by_class_name("GeneralStats-row")
    for team in table:
        stats = team.find_element_by_class_name("GeneralStats-item--club")
        clubName = stats.find_element_by_class_name("mobile-item")
        leaderboard.append(clubName.get_attribute('innerHTML'))
    driver.close()
    return leaderboard

def getIndividualStats(elem, gameNb):
    ret = []
    ret.append(gameNb)
    stats = elem.find_elements_by_class_name("GeneralStats-item")
    # for stat in stats:
    #     print(stat.get_attribute('innerHTML'))
    # print()
    ret.append(stats[1].find_element_by_class_name("mobile-item").get_attribute('innerHTML'))
    ret.append(int(stats[2].get_attribute('innerHTML')))
    ret.append(int(stats[4].get_attribute('innerHTML')))
    ret.append(int(stats[5].get_attribute('innerHTML')))
    ret.append(int(stats[6].get_attribute('innerHTML')))
    ret.append(int(stats[7].get_attribute('innerHTML')))
    ret.append(int(stats[8].get_attribute('innerHTML')))
    if (stats[9].get_attribute('innerHTML')[0] == '+'):
        ret.append(int(stats[9].get_attribute('innerHTML')[1:]))
    else:
        ret.append(int(stats[9].get_attribute('innerHTML')))
    return ret

def getAll(url):
    all = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "didomi-continue-without-agreeing")):
        continueWithoutAgreeing = driver.find_element_by_class_name("didomi-continue-without-agreeing")
        actions = ActionChains(driver)
        actions.click(continueWithoutAgreeing).perform()
    table = driver.find_elements_by_class_name("GeneralStats-row")
    for team in table:
        all.append(getIndividualStats(team, int(url.split('=')[-1])))
    driver.close()
    return all

def getStandingsDay(url):
    ret = []
    ret.append(getLeaderboard(url))
    all = getAll(url)
    for place in all:
        ret.append(place)
    return ret

def getStandings(url, post):
    standings = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "didomi-continue-without-agreeing")):
        continueWithoutAgreeing = driver.find_element_by_class_name("didomi-continue-without-agreeing")
        actions = ActionChains(driver)
        actions.click(continueWithoutAgreeing).perform()
    select = Select(driver.find_element_by_name('matchDay'))
    nbDays = []
    for option in select.options:
        nbDays.append(int(option.get_attribute("innerHTML").split("Journée ")[1].split('\n')[0]))
    driver.close()
    printProgressBar(0, len(nbDays), prefix="   Progress:", suffix="Complete (0/"+str(len(nbDays))+")")
    for i in range(max(nbDays)):
        currentUrl = url + post + str(i+1)
        standings.append(getStandingsDay(currentUrl))
        printProgressBar(i+1, len(nbDays), prefix="   Progress:", suffix="Complete ("+str(i+1)+"/"+str(len(nbDays))+")")
    return standings

preUrl = "https://www.ligue2.fr/classement?seasonId="
postUrl = "&matchDay="
url = ""
if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
for i in range(nbYearToGet):
    print("Getting data for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    url = preUrl + str(int(year)-i) + "-" + str(int(year)-i+1)
    datas = getStandings(url, postUrl)
    standings = []
    first = []
    second = []
    third = []
    four = []
    five = []
    six = []
    seven = []
    height = []
    nine = []
    ten = []
    eleven = []
    twelve = []
    thirteen = []
    fourteen = []
    fifteen = []
    sixteen = []
    seventeen = []
    heighteen = []
    nineteen = []
    twenty = []
    for day in datas:
        standings.append(day[0])
        first.append(day[1])
        second.append(day[2])
        third.append(day[3])
        four.append(day[4])
        five.append(day[5])
        six.append(day[6])
        seven.append(day[7])
        height.append(day[8])
        nine.append(day[9])
        ten.append(day[10])
        eleven.append(day[11])
        twelve.append(day[12])
        thirteen.append(day[13])
        fourteen.append(day[14])
        fifteen.append(day[15])
        sixteen.append(day[16])
        seventeen.append(day[17])
        heighteen.append(day[18])
        nineteen.append(day[19])
        twenty.append(day[20])
    try:
        os.makedirs(str(int(year)-i)+"-"+str(int(year)-i+1))
    except FileExistsError:
        pass
    headerStanding = ["leagueMatchNb", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th"]
    headerPlaceOverTime =["leagueMatchNb", "teamName", "points", "wins", "draws", "loses", "goalsFor", "goalsAgainst", "goalsDiff"]
    pd.DataFrame(standings).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_standing.csv", header=headerStanding, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_standing.csv")
    pd.DataFrame(first).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_1stPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_1stPlaceOverTime.csv")
    pd.DataFrame(second).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_2ndPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_2ndPlaceOverTime.csv")
    pd.DataFrame(third).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_3rdPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_3rdPlaceOverTime.csv")
    pd.DataFrame(four).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_4thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_4thPlaceOverTime.csv")
    pd.DataFrame(five).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_5thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_5thPlaceOverTime.csv")
    pd.DataFrame(six).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_6thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_6thPlaceOverTime.csv")
    pd.DataFrame(seven).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_7thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_7thPlaceOverTime.csv")
    pd.DataFrame(height).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_8thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_8thPlaceOverTime.csv")
    pd.DataFrame(nine).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_9thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_9thPlaceOverTime.csv")
    pd.DataFrame(ten).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_10thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_10thPlaceOverTime.csv")
    pd.DataFrame(eleven).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_11thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_11thPlaceOverTime.csv")
    pd.DataFrame(twelve).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_12thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_12thPlaceOverTime.csv")
    pd.DataFrame(thirteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_13thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_13thPlaceOverTime.csv")
    pd.DataFrame(fourteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_14thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_14thPlaceOverTime.csv")
    pd.DataFrame(fifteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_15thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_15thPlaceOverTime.csv")
    pd.DataFrame(sixteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_16thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_16thPlaceOverTime.csv")
    pd.DataFrame(seventeen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_17thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_17thPlaceOverTime.csv")
    pd.DataFrame(heighteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_18thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_18thPlaceOverTime.csv")
    pd.DataFrame(nineteen).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_19thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_19thPlaceOverTime.csv")
    pd.DataFrame(twenty).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_20thPlaceOverTime.csv", header=headerPlaceOverTime, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_20thPlaceOverTime.csv")
    print()

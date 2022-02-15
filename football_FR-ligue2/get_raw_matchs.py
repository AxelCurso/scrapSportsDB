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
from selenium.common.exceptions import ElementNotInteractableException

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

def check_exists_by_id(d, c):
    try:
        d.find_element_by_id(c)
    except NoSuchElementException:
        return False
    return True

def getSingleStats(url):
    stats = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "didomi-continue-without-agreeing")):
        continueWithoutAgreeing = driver.find_element_by_class_name("didomi-continue-without-agreeing")
        actions = ActionChains(driver)
        actions.click(continueWithoutAgreeing).perform()
    while (check_exists_by_id(driver, "nav-title-matchpage-stats") == False):
        continue
    nav = driver.find_element_by_id("nav-title-matchpage-stats")
    actions = ActionChains(driver)
    actions.click(nav).perform()
    # matchInfos
    stats.append(int(url.split("=")[-1]))
    infos = driver.find_elements_by_class_name("MatchHeader-text")[0].get_attribute('innerHTML').split(" - ")
    date = infos[0].split('\n')
    hour = infos[1].split('\n')
    home = []
    away = []
    all = driver.find_elements_by_class_name("Opta-Stats-Bars")
    while (all == []):
        all = driver.find_elements_by_class_name("Opta-Stats-Bars")
    for section in all:
        for stat in section.find_elements_by_class_name("Opta-Outer"):
            if (stat.get_attribute('innerHTML') == "-"):
                driver.close()
                return []
    # TODO
    splitDate = date[1].split(' ')
    stats.append(splitDate[-4] + "-" + splitDate[-3] + "-" + splitDate[-2] + "-" + splitDate[-1])
    stats.append(int(hour[0].split(':')[0] + hour[0].split(':')[1]))
    stats.append(int(driver.find_element_by_class_name("MatchHeader-day").get_attribute('innerHTML').split(' ')[-1]))
    stats.append(driver.find_element_by_class_name("home").find_element_by_class_name("MatchHeader-clubName").get_attribute('innerHTML'))
    stats.append(driver.find_element_by_class_name("away").find_element_by_class_name("MatchHeader-clubName").get_attribute('innerHTML'))
    score = driver.find_element_by_class_name("MatchHeader-scoreResult").get_attribute('innerHTML').split('-')
    stats.append(int(score[0]))
    stats.append(int(score[1]))
    # general
    general = all[0]
    generalStats = general.find_elements_by_class_name("Opta-Outer")
    home.append(float(generalStats[0].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[0].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(float(generalStats[2].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[2].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(float(generalStats[4].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[4].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(int(generalStats[6].get_attribute('innerHTML')))
    home.append(int(generalStats[8].get_attribute('innerHTML')))
    home.append(int(generalStats[10].get_attribute('innerHTML')))
    away.append(float(generalStats[1].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[1].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(float(generalStats[3].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[3].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(float(generalStats[5].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + generalStats[5].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(int(generalStats[7].get_attribute('innerHTML')))
    away.append(int(generalStats[9].get_attribute('innerHTML')))
    away.append(int(generalStats[11].get_attribute('innerHTML')))
    # distribution
    distribution = all[1]
    distributionStats = distribution.find_elements_by_class_name("Opta-Outer")
    home.append(int(distributionStats[0].get_attribute('innerHTML')))
    home.append(int(distributionStats[2].get_attribute('innerHTML')))
    home.append(float(distributionStats[4].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[4].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(float(distributionStats[6].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[6].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(int(distributionStats[8].get_attribute('innerHTML')))
    home.append(float(distributionStats[10].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[10].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(int(distributionStats[1].get_attribute('innerHTML')))
    away.append(int(distributionStats[3].get_attribute('innerHTML')))
    away.append(float(distributionStats[5].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[5].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(float(distributionStats[7].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[7].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(int(distributionStats[9].get_attribute('innerHTML')))
    away.append(float(distributionStats[11].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + distributionStats[11].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    # attack
    attack = all[2]
    attackStats = attack.find_elements_by_class_name("Opta-Outer")
    home.append(int(attackStats[0].get_attribute('innerHTML')))
    home.append(int(attackStats[2].get_attribute('innerHTML')))
    home.append(int(attackStats[4].get_attribute('innerHTML')))
    home.append(int(attackStats[6].get_attribute('innerHTML')))
    home.append(int(attackStats[8].get_attribute('innerHTML')))
    home.append(int(attackStats[10].get_attribute('innerHTML')))
    home.append(float(attackStats[12].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + attackStats[12].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(int(attackStats[1].get_attribute('innerHTML')))
    away.append(int(attackStats[3].get_attribute('innerHTML')))
    away.append(int(attackStats[5].get_attribute('innerHTML')))
    away.append(int(attackStats[7].get_attribute('innerHTML')))
    away.append(int(attackStats[9].get_attribute('innerHTML')))
    away.append(int(attackStats[11].get_attribute('innerHTML')))
    away.append(float(attackStats[13].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + attackStats[13].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    # defense
    defense = all[3]
    defenseStats = defense.find_elements_by_class_name("Opta-Outer")
    home.append(int(defenseStats[0].get_attribute('innerHTML')))
    home.append(float(defenseStats[2].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + defenseStats[2].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    home.append(int(defenseStats[4].get_attribute('innerHTML')))
    away.append(int(defenseStats[1].get_attribute('innerHTML')))
    away.append(float(defenseStats[3].get_attribute('innerHTML').split("&")[0].split(",")[0]) + float("0." + defenseStats[3].get_attribute('innerHTML').split('&')[0].split(',')[1]))
    away.append(int(defenseStats[5].get_attribute('innerHTML')))
    # discipline
    discipline = all[4]
    disciplineStats = discipline.find_elements_by_class_name("Opta-Outer")
    home.append(int(disciplineStats[0].get_attribute('innerHTML')))
    home.append(int(disciplineStats[2].get_attribute('innerHTML')))
    home.append(int(disciplineStats[4].get_attribute('innerHTML')))
    away.append(int(disciplineStats[1].get_attribute('innerHTML')))
    away.append(int(disciplineStats[3].get_attribute('innerHTML')))
    away.append(int(disciplineStats[5].get_attribute('innerHTML')))
    for homeStat in home:
        stats.append(homeStat)
    for awayStat in away:
        stats.append(awayStat)
    driver.close()
    return stats

def getMatchStats(url):
    stats = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "didomi-continue-without-agreeing")):
        continueWithoutAgreeing = driver.find_element_by_class_name("didomi-continue-without-agreeing")
        actions = ActionChains(driver)
        actions.click(continueWithoutAgreeing).perform()
    matchs = driver.find_elements_by_class_name("match-result")
    goodMatchs = []
    for match in matchs:
        if (match.find_element_by_class_name("result").find_element_by_tag_name("span").find_element_by_tag_name("span").get_attribute('innerHTML').isnumeric()):
            goodMatchs.append(match.get_attribute("id").split('_')[0])
    driver.close()
    preUrl = "https://www.ligue2.fr/feuille-match?matchId="
    for current in goodMatchs:
        newUrl = preUrl + current
        resCurrent = []
        try:
            resCurrent = getSingleStats(newUrl)
        except ElementNotInteractableException:
            resCurrent = []
        if (resCurrent):
            stats.append(resCurrent)
    # print(stats)
    return stats

def getMatchs(preUrl, postUrl):
    matchs = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(preUrl)
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
    for day in range(max(nbDays)):
        url = preUrl + postUrl + str(day+1)
        matchs.append(getMatchStats(url))
        printProgressBar(day+1, len(nbDays), prefix="   Progress:", suffix="Complete ("+str(day+1)+"/"+str(len(nbDays))+")")
    return matchs

preUrl = "https://www.ligue2.fr/calendrier-resultats?seasonId="
postUrl = "&matchDay="
url = ""
if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
header = ["id", "date", "hour", "leagueMatchNb", "idHome", "homeTeam", "idAway", "awayTeam", "h_score", "a_score", "h_possession", "h_duelsWon", "h_aerialDuelsWon", "h_interceptions", "h_offPlays", "h_corners", "h_passes", "h_longPasses", "h_succeededPasses", "h_succeededPassesOppositeSide", "h_centers", "h_succeededCenters", "h_shots", "h_targetedShots", "h_counteredShots", "h_extSurfaceShots", "h_intSurfaceShots", "h_precisionShots", "h_tackles", "h_succeededTackles", "h_clears", "h_concededFaults", "h_yellowCards", "h_redCards", "a_possession", "a_duelsWon", "a_aerialDuelsWon", "a_interceptions", "a_offPlays", "a_corners", "a_passes", "a_longPasses", "a_succeededPasses", "a_succeededPassesOppositeSide", "a_centers", "a_succeededCenters", "a_shots", "a_targetedShots", "a_counteredShots", "a_extSurfaceShots", "a_intSurfaceShots", "a_precisionShots", "a_tackles", "a_succeededTackles", "a_clears", "a_concededFaults", "a_yellowCards", "a_redCards"]
for i in range(nbYearToGet):
    allMatchs = []
    matchs = []
    print("Getting data for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    url = preUrl + str(int(year)-i) + "-" + str(int(year)-i+1)
    matchs = getMatchs(url, postUrl)
    for day in matchs:
        for match in day:
            allMatchs.append(match)
    pd.DataFrame(allMatchs).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_matchs.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_matchs.csv")
    print()

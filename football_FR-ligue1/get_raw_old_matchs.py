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

def check_exists_by_tag(d, c):
    try:
        d.find_element_by_tag_name(c)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_class(d, c):
    try:
        d.find_element_by_class_name(c)
    except NoSuchElementException:
        return False
    return True

def getGeneralInfos(tab):
    home = []
    away = []
    ret = []
    for i in range(len(tab)):
        if check_exists_by_tag(tab[i], "th"):
            th = tab[i].find_element_by_tag_name("th").get_attribute("innerHTML")
            if th == "Possession":
                i += 1
                possessions = [int(elem.get_attribute("innerHTML")[:-1]) for elem in tab[i].find_elements_by_tag_name("strong")]
                home.append(possessions[0])
                away.append(possessions[1])
            elif th == "Passing Accuracy":
                continue
            elif th == "Shots on Target":
                continue
            elif th == "Saves":
                continue
            elif th == "Cards":
                continue
    ret.append(home)
    ret.append(away)
    return ret

def getSummaryInfos(summary):
    home = [None]*6
    away = [None]*6
    ret = []
    for info in summary[0]:
        thing = info.get_attribute("data-stat")
        if (thing == "shots_total"):
            home[0] = int(info.get_attribute("innerHTML"))
        elif (thing == "shots_on_target"):
            home[1] = int(info.get_attribute("innerHTML"))
        elif (thing == "cards_yellow"):
            home[2] = int(info.get_attribute("innerHTML"))
        elif (thing == "cards_red"):
            home[3] = int(info.get_attribute("innerHTML"))
        elif (thing == "tackles"):
            home[4] = int(info.get_attribute("innerHTML"))
        elif (thing == "interceptions"):
            home[5] = int(info.get_attribute("innerHTML"))
    for info in summary[1]:
        thing = info.get_attribute("data-stat")
        if (thing == "shots_total"):
            away[0] = int(info.get_attribute("innerHTML"))
        elif (thing == "shots_on_target"):
            away[1] = int(info.get_attribute("innerHTML"))
        elif (thing == "cards_yellow"):
            away[2] = int(info.get_attribute("innerHTML"))
        elif (thing == "cards_red"):
            away[3] = int(info.get_attribute("innerHTML"))
        elif (thing == "tackles"):
            away[4] = int(info.get_attribute("innerHTML"))
        elif (thing == "interceptions"):
            away[5] = int(info.get_attribute("innerHTML"))
    ret.append(home)
    ret.append(away)
    return ret

def getPassingInfos(passing):
    home = [None]*2
    away = [None]*2
    ret = []
    for info in summary[0]:
        thing = info.get_attribute("data-stat")
        if (thing == "passes"):
            home[0] = int(info.get_attribute("innerHTML"))
        elif (thing == "passes_pct"):
            home[1] = int(info.get_attribute("innerHTML"))
    for info in summary[1]:
        thing = info.get_attribute("data-stat")
        if (thing == "passes"):
            away[0] = int(info.get_attribute("innerHTML"))
        elif (thing == "passes_pct"):
            away[1] = int(info.get_attribute("innerHTML"))
    ret.append(home)
    ret.append(away)
    return ret

def getPassingTypesInfos(passing_types):
    home = []
    away = []
    ret = []
    for info in summary[0]:
        thing = info.get_attribute("data-stat")
    for info in summary[1]:
        thing = info.get_attribute("data-stat")
    ret.append(home)
    ret.append(away)
    return ret

def getDefenseInfos(defense):
    home = []
    away = []
    ret = []
    for info in summary[0]:
        print(info)
    for info in summary[1]:
        print(info)
    ret.append(home)
    ret.append(away)
    return ret

def getPossessionInfos(possession):
    home = []
    away = []
    ret = []
    for info in summary[0]:
        print(info)
    for info in summary[1]:
        print(info)
    ret.append(home)
    ret.append(away)
    return ret

def getMiscInfos(misc):
    home = []
    away = []
    ret = []
    for info in summary[0]:
        print(info)
    for info in summary[1]:
        print(info)
    ret.append(home)
    ret.append(away)
    return ret

def getSingleMatchStats(url):
    stats = []
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    driver.get(url)
    if (check_exists_by_class(driver, "qc-cmp2-summary-buttons")):
        continueWithoutAgree = driver.find_element_by_class_name("qc-cmp2-summary-buttons")
        buttons = continueWithoutAgree.find_elements_by_tag_name("button")
        actions = ActionChains(driver)
        actions.click(buttons[2]).perform()
    stats.append(int(url.split('/')[-2], base=16))
    venuetime = driver.find_element_by_class_name("venuetime")
    date = venuetime.get_attribute("data-venue-date").split('-')
    stats.append(int(date[0]+date[1]+date[2]))
    hour = venuetime.get_attribute("data-venue-time").split(':')
    stats.append(int(hour[0]+hour[1]))
    stats.append(int(driver.find_element_by_id("content").find_element_by_tag_name("div").get_attribute("innerHTML").split(' ')[-1].split(')')[0]))
    stats.append(url.split('/')[-1].split('-')[0])
    stats.append(url.split('/')[-1].split('-')[1])
    scores = [int(elem.find_element_by_class_name("score").get_attribute("innerHTML")) for elem in driver.find_elements_by_class_name("scores")]
    stats.append(scores[0])
    stats.append(scores[1])
    tabGeneral = driver.find_element_by_id("team_stats").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    infosGeneral = getGeneralInfos(tabGeneral)
    teamIds = [k.find_element_by_tag_name("img").get_attribute("src").split('/')[-1].split('.')[0] for k in driver.find_element_by_class_name("scorebox").find_elements_by_class_name("logo")]
    summary = [driver.find_element_by_id("div_stats_"+k+"_summary").find_element_by_tag_name("tfoot").find_elements_by_tag_name("td") for k in teamIds]
    passing = [driver.find_element_by_id("div_stats_"+k+"_passing").find_element_by_tag_name("tfoot").find_elements_by_tag_name("td") for k in teamIds]
    passing_types = [driver.find_element_by_id("div_stats_"+k+"_passing_types").find_element_by_tag_name("tfoot").find_elements_by_tag_name("td") for k in teamIds]
    defense = [driver.find_element_by_id("div_stats_"+k+"_defense").find_element_by_tag_name("tfoot").find_elements_by_tag_name("td") for k in teamIds]
    possession = [driver.find_element_by_id("div_stats_"+k+"_possession").find_element_by_tag_name("tfoot").find_elements_by_tag_name("td") for k in teamIds]
    misc = [driver.find_element_by_id("div_stats_"+k+"_misc").find_element_by_tag_name("tfoot") .find_elements_by_tag_name("td")for k in teamIds]
    infosSummary = getSummaryInfos(summary)
    infosPassing = getPassingInfos(passing)
    infosPassingTypes = getPassingTypesInfos(passing_types)
    infosDefense = getDefenseInfos(defense)
    infosPossession = getPossessionInfos(possession)
    infosMisc = getMiscInfos(misc)
    # HOME
    for info in infosGeneral[0]:
        stats.append(info)
    # AWAY
    for info in infosGeneral[1]:
        stats.append(info)
    print(stats)
    while (1):
        continue
    driver.close()
    return stats

def getMatchsStats(url):
    matchs = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
    # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
    postUrl = "-Scores-and-Fixtures"
    newUrl = "".join([k+"/" for k in url.split('/')[:-2]]) + "schedule/" + url.split('/')[-1] + postUrl
    driver.get(newUrl)
    if (check_exists_by_class(driver, "qc-cmp2-summary-buttons")):
        continueWithoutAgree = driver.find_element_by_class_name("qc-cmp2-summary-buttons")
        buttons = continueWithoutAgree.find_elements_by_tag_name("button")
        actions = ActionChains(driver)
        actions.click(buttons[2]).perform()
    tab = driver.find_element_by_class_name("stats_table").find_element_by_tag_name("tbody")
    rows = tab.find_elements_by_tag_name("tr")
    elems = []
    for row in rows:
        if (row.get_attribute("class") == ""):
            elems.append(row.find_elements_by_tag_name("td")[-2].find_element_by_tag_name("a").get_attribute("href"))
    driver.close()
    for elem in elems:
        if not "History" in elem:
            # print(elem)
            matchs.append(getSingleMatchStats(elem).copy())
    return matchs

# base = "https://fbref.com/"
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome("/home/axel/chromedriver", options=chrome_options)
# # driver = webdriver.Chrome("/Users/axelcurso/chromedriver", options=chrome_options)
# driver.get("https://fbref.com/en/comps/13/history/Ligue-1-Seasons")
# if (check_exists_by_class(driver, "qc-cmp2-summary-buttons")):
#     continueWithoutAgree = driver.find_element_by_class_name("qc-cmp2-summary-buttons")
#     buttons = continueWithoutAgree.find_elements_by_tag_name("button")
#     actions = ActionChains(driver)
#     actions.click(buttons[2]).perform()
# tab = driver.find_element_by_class_name("stats_table")
# trs = tab.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")[2:]
# links = [tr.find_element_by_tag_name("a").get_attribute('href') for tr in trs]
# driver.close()
# header = ["id", "date", "hour", "leagueMatchNb", "homeTeam", "awayTeam", "h_score", "a_score", "h_possession", "h_duelsWon", "h_aerialDuelsWon", "h_interceptions", "h_offPlays", "h_corners", "h_passes", "h_longPasses", "h_succeededPasses", "h_succeededPassesOppositeSide", "h_centers", "h_succeededCenters", "h_shots", "h_targetedShots", "h_counteredShots", "h_extSurfaceShots", "h_intSurfaceShots", "h_precisionShots", "h_tackles", "h_succeededTackles", "h_clears", "h_concededFaults", "h_yellowCards", "h_redCards", "a_possession", "a_duelsWon", "a_aerialDuelsWon", "a_interceptions", "a_offPlays", "a_corners", "a_passes", "a_longPasses", "a_succeededPasses", "a_succeededPassesOppositeSide", "a_centers", "a_succeededCenters", "a_shots", "a_targetedShots", "a_counteredShots", "a_extSurfaceShots", "a_intSurfaceShots", "a_precisionShots", "a_tackles", "a_succeededTackles", "a_clears", "a_concededFaults", "a_yellowCards", "a_redCards"]
# # for link in links[0:1]:
# #     yearInStr = link.split('/')[-1].split('-')[0]+"-"+link.split('/')[-1].split('-')[1]
# #     print("Getting data for year: " + yearInStr)
# #     matchs = []
# #     matchs = getMatchsStats(link)
# #     # pd.DataFrame(matchs).to_csv(yearInStr+"/raw_matchs.csv")
# #     print("   Data saved: " + yearInStr+"/raw_matchs.csv")
# #     print()
print(getSingleMatchStats("https://fbref.com/en/matches/6a07521d/Montpellier-Troyes-January-19-2022-Ligue-1"))

import pandas as pd
import numpy as np
import sys
import os
import time
from datetime import date
import math

def strToInt(str):
    months = {"JANVIER": "01", "FÉVRIER": "02", "MARS": "03", "AVRIL": "04", "MAI": "05", "JUIN": "06", "JUILLET": "07", "AOÛT": "08", "SEPTEMBRE": "09", "OCTOBRE": "10", "NOVEMBRE": "11", "DÉCEMBRE": "12"}
    splitted = str.split('-')
    return (splitted[3] + months[splitted[2]] + splitted[1])

if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
namesToIds = pd.read_csv("NameToIds.csv")
header = ["id", "date", "hour", "leagueMatchNb", "idHome", "homeTeam", "idAway", "awayTeam", "h_score", "a_score", "h_possession", "h_duelsWon", "h_aerialDuelsWon", "h_interceptions", "h_offPlays", "h_corners", "h_passes", "h_longPasses", "h_succeededPasses", "h_succeededPassesOppositeSide", "h_centers", "h_succeededCenters", "h_shots", "h_targetedShots", "h_counteredShots", "h_extSurfaceShots", "h_intSurfaceShots", "h_precisionShots", "h_tackles", "h_succeededTackles", "h_clears", "h_concededFaults", "h_yellowCards", "h_redCards", "a_possession", "a_duelsWon", "a_aerialDuelsWon", "a_interceptions", "a_offPlays", "a_corners", "a_passes", "a_longPasses", "a_succeededPasses", "a_succeededPassesOppositeSide", "a_centers", "a_succeededCenters", "a_shots", "a_targetedShots", "a_counteredShots", "a_extSurfaceShots", "a_intSurfaceShots", "a_precisionShots", "a_tackles", "a_succeededTackles", "a_clears", "a_concededFaults", "a_yellowCards", "a_redCards"]
pd.set_option('display.max_columns', None)
for i in range(nbYearToGet):
    print("Changing abbreviations' team for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    dict_lookup = dict(zip(namesToIds['ligue1'], namesToIds['abbr']))
    dictIds = dict(zip(namesToIds['abbr'], namesToIds['id']))
    # dict_lookup = {k: dict[k] for k in dict if isinstance(k, str)}
    if year >= 2020:
        matchs = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_matchs.csv")
        # print(matchs.head())
        matchs["a_succeededCenters"] = matchs["a_centers"]
        matchs["a_centers"] = matchs["a_succeededPassesOppositeSide"]
        matchs["a_succeededPassesOppositeSide"] = matchs["a_succeededPasses"]
        matchs["a_succeededPasses"] = matchs["a_longPasses"]
        matchs["a_longPasses"] = matchs["a_passes"]
        matchs["a_passes"] = matchs["a_corners"]
        matchs["a_corners"] = matchs["a_offPlays"]
        matchs["a_offPlays"] = matchs["a_interceptions"]
        matchs["a_interceptions"] = matchs["a_aerialDuelsWon"]
        matchs["a_aerialDuelsWon"] = matchs["a_duelsWon"]
        matchs["a_duelsWon"] = matchs["a_possession"]
        matchs["a_possession"] = matchs["h_redCards"]
        matchs["h_redCards"] = matchs["h_yellowCards"]
        matchs["h_yellowCards"] = matchs["h_concededFaults"]
        matchs["h_concededFaults"] = matchs["h_clears"]
        matchs["h_clears"] = matchs["h_succeededTackles"]
        matchs["h_succeededTackles"] = matchs["h_tackles"]
        matchs["h_tackles"] = matchs["h_precisionShots"]
        matchs["h_precisionShots"] = matchs["h_intSurfaceShots"]
        matchs["h_intSurfaceShots"] = matchs["h_extSurfaceShots"]
        matchs["h_extSurfaceShots"] = matchs["h_counteredShots"]
        matchs["h_counteredShots"] = matchs["h_targetedShots"]
        matchs["h_targetedShots"] = matchs["h_shots"]
        matchs["h_shots"] = matchs["h_succeededCenters"]
        matchs["h_succeededCenters"] = matchs["h_succeededPassesOppositeSide"]
        matchs["h_centers"] = matchs["h_succeededPasses"]
        matchs["h_succeededPassesOppositeSide"] = matchs["h_longPasses"]
        matchs["h_succeededPasses"] = matchs["h_passes"]
        matchs["h_longPasses"] = matchs["h_corners"]
        matchs["h_passes"] = matchs["h_offPlays"]
        matchs["h_corners"] = matchs["h_interceptions"]
        matchs["h_offPlays"] = matchs["h_aerialDuelsWon"]
        matchs["h_interceptions"] = matchs["h_duelsWon"]
        matchs["h_aerialDuelsWon"] = matchs["h_possession"]
        matchs["h_duelsWon"] = matchs["a_score"]
        matchs["h_possession"] = matchs["h_score"]
        matchs["a_score"] = matchs["awayTeam"]
        matchs["h_score"] = matchs["idAway"]
        matchs["awayTeam"] = matchs["homeTeam"]
        matchs["homeTeam"] = matchs["idHome"]
        matchs['awayTeam'] = [dict_lookup[item] for item in matchs['awayTeam']]
        matchs['homeTeam'] = [dict_lookup[item] for item in matchs['homeTeam']]
        matchs['idHome'] = [dictIds[item] for item in matchs['homeTeam']]
        matchs['idAway'] = [dictIds[item] for item in matchs['awayTeam']]
        matchs['date'] = [strToInt(item) for item in matchs['date']]
        print(matchs)
        matchs.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_matchs.csv", header=header, index=None)
        print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_matchs.csv")

    one = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_1stPlaceOverTime.csv")
    two = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_2ndPlaceOverTime.csv")
    three = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_3rdPlaceOverTime.csv")
    four = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_4thPlaceOverTime.csv")
    five = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_5thPlaceOverTime.csv")
    six = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_6thPlaceOverTime.csv")
    seven = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_7thPlaceOverTime.csv")
    height = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_8thPlaceOverTime.csv")
    nine = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_9thPlaceOverTime.csv")
    ten = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_10thPlaceOverTime.csv")
    eleven = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_11thPlaceOverTime.csv")
    twelve = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_12thPlaceOverTime.csv")
    thirteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_13thPlaceOverTime.csv")
    fourteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_14thPlaceOverTime.csv")
    fifteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_15thPlaceOverTime.csv")
    sixteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_16thPlaceOverTime.csv")
    seventeen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_17thPlaceOverTime.csv")
    heighteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_18thPlaceOverTime.csv")
    nineteen = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_19thPlaceOverTime.csv")
    twenty = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_20thPlaceOverTime.csv")
    standing = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/raw_standing.csv")

    header = ["leagueMatchNb","teamName","points","wins","draws","loses","goalsFor","goalsAgainst","goalsDiff"]
    headerStanding = ["leagueMatchNb","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th","13th","14th","15th","16th","17th","18th","19th","20th"]
    one['teamName'] = [dict_lookup[item] for item in one['teamName']]
    two['teamName'] = [dict_lookup[item] for item in two['teamName']]
    three['teamName'] = [dict_lookup[item] for item in three['teamName']]
    four['teamName'] = [dict_lookup[item] for item in four['teamName']]
    five['teamName'] = [dict_lookup[item] for item in five['teamName']]
    six['teamName'] = [dict_lookup[item] for item in six['teamName']]
    seven['teamName'] = [dict_lookup[item] for item in seven['teamName']]
    height['teamName'] = [dict_lookup[item] for item in height['teamName']]
    nine['teamName'] = [dict_lookup[item] for item in nine['teamName']]
    ten['teamName'] = [dict_lookup[item] for item in ten['teamName']]
    eleven['teamName'] = [dict_lookup[item] for item in eleven['teamName']]
    twelve['teamName'] = [dict_lookup[item] for item in twelve['teamName']]
    thirteen['teamName'] = [dict_lookup[item] for item in thirteen['teamName']]
    fourteen['teamName'] = [dict_lookup[item] for item in fourteen['teamName']]
    fifteen['teamName'] = [dict_lookup[item] for item in fifteen['teamName']]
    sixteen['teamName'] = [dict_lookup[item] for item in sixteen['teamName']]
    seventeen['teamName'] = [dict_lookup[item] for item in seventeen['teamName']]
    heighteen['teamName'] = [dict_lookup[item] for item in heighteen['teamName']]
    nineteen['teamName'] = [dict_lookup[item] for item in nineteen['teamName']]
    twenty['teamName'] = [dict_lookup[item] for item in twenty['teamName']]
    standing['1st'] = [dict_lookup[item] for item in standing['1st']]
    standing['2nd'] = [dict_lookup[item] for item in standing['2nd']]
    standing['3rd'] = [dict_lookup[item] for item in standing['3rd']]
    standing['4th'] = [dict_lookup[item] for item in standing['4th']]
    standing['5th'] = [dict_lookup[item] for item in standing['5th']]
    standing['6th'] = [dict_lookup[item] for item in standing['6th']]
    standing['7th'] = [dict_lookup[item] for item in standing['7th']]
    standing['8th'] = [dict_lookup[item] for item in standing['8th']]
    standing['9th'] = [dict_lookup[item] for item in standing['9th']]
    standing['10th'] = [dict_lookup[item] for item in standing['10th']]
    standing['11th'] = [dict_lookup[item] for item in standing['11th']]
    standing['12th'] = [dict_lookup[item] for item in standing['12th']]
    standing['13th'] = [dict_lookup[item] for item in standing['13th']]
    standing['14th'] = [dict_lookup[item] for item in standing['14th']]
    standing['15th'] = [dict_lookup[item] for item in standing['15th']]
    standing['16th'] = [dict_lookup[item] for item in standing['16th']]
    standing['17th'] = [dict_lookup[item] for item in standing['17th']]
    standing['18th'] = [dict_lookup[item] for item in standing['18th']]
    standing['19th'] = [dict_lookup[item] for item in standing['19th']]
    standing['20th'] = [dict_lookup[item] for item in standing['20th']]

    one.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_1stPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_1stPlaceOverTime.csv")
    two.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_2ndPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_2ndthPlaceOverTime.csv")
    three.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_3rdPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_3rdthPlaceOverTime.csv")
    four.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_4thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_4thPlaceOverTime.csv")
    five.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_5thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_5thPlaceOverTime.csv")
    six.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_6thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_6thPlaceOverTime.csv")
    seven.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_7thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_7thPlaceOverTime.csv")
    height.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_8thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_8thPlaceOverTime.csv")
    nine.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_9thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_9thPlaceOverTime.csv")
    ten.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_10thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_10thPlaceOverTime.csv")
    eleven.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_11thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_11thPlaceOverTime.csv")
    twelve.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_12thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_12thPlaceOverTime.csv")
    thirteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_13thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_13thPlaceOverTime.csv")
    fourteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_14thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_14thPlaceOverTime.csv")
    fifteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_15thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_15thPlaceOverTime.csv")
    sixteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_16thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_16thPlaceOverTime.csv")
    seventeen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_17thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_17thPlaceOverTime.csv")
    heighteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_18thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_18thPlaceOverTime.csv")
    nineteen.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_19thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_19thPlaceOverTime.csv")
    twenty.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_20thPlaceOverTime.csv", header=header, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_10thPlaceOverTime.csv")
    standing.to_csv(str(int(year)-i)+"-"+str(int(year)-i+1) + "/final_standing.csv", header=headerStanding, index=None)
    print("   Data saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/final_standing.csv")
    print()

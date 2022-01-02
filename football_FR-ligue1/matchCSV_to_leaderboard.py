import pandas as pd
import numpy as np
import sys
import time
from datetime import date

def getStatsOverGames(df, team):
    home = df.loc[df["homeTeam"] == team]
    away = df.loc[df["awayTeam"] == team]
    nbGames = len(home) + len(away)
    # print(nbGames)
    stats = []
    for i in range(nbGames):
        gameStats = []
        if (i+1 in home["leagueMatchNb"].values):
            game = home.loc[home["leagueMatchNb"] == i+1]
            # if (team == "OL"):
            #     print(game)
            if (game.empty == False):
                # print(game["id"].values[0])
                gameStats.append(game["idHome"].values[0])
                gameStats.append(game["homeTeam"].values[0])
                if (game["h_score"].values[0] > game["a_score"].values[0]):
                    if (i == 0):
                        gameStats.append(3)
                        gameStats.append(1)
                        gameStats.append(0)
                        gameStats.append(0)
                    else:
                        gameStats.append(stats[-1][2] + 3)
                        gameStats.append(stats[-1][3] + 1)
                        gameStats.append(stats[-1][4])
                        gameStats.append(stats[-1][5])
                elif (game["h_score"].values[0] == game["a_score"].values[0]):
                    if (i == 0):
                        gameStats.append(1)
                        gameStats.append(0)
                        gameStats.append(1)
                        gameStats.append(0)
                    else:
                        gameStats.append(stats[-1][2] + 1)
                        gameStats.append(stats[-1][3])
                        gameStats.append(stats[-1][4] + 1)
                        gameStats.append(stats[-1][5])
                else:
                    if (i == 0):
                        gameStats.append(0)
                        gameStats.append(0)
                        gameStats.append(0)
                        gameStats.append(1)
                    else:
                        gameStats.append(stats[-1][2])
                        gameStats.append(stats[-1][3])
                        gameStats.append(stats[-1][4])
                        gameStats.append(stats[-1][5] + 1)
                if (i == 0):
                    gameStats.append(game["h_score"].values[0])
                    gameStats.append(game["a_score"].values[0])
                    gameStats.append(gameStats[-2] - gameStats[-1])
                else:
                    gameStats.append(stats[-1][6] + game["h_score"].values[0])
                    gameStats.append(stats[-1][7] + game["a_score"].values[0])
                    gameStats.append(gameStats[-2] - gameStats[-1])
                gameStats.append(int(i+1))
                # print(gameStats)
                stats.append(gameStats)
        elif (i+1 in away["leagueMatchNb"].values):
            game = away.loc[away["leagueMatchNb"] == i+1]
            # if (team == "OL"):
            #     print(game)
            if (game.empty == False):
                # print(game["id"].values[0])
                gameStats.append(game["idAway"].values[0])
                gameStats.append(game["awayTeam"].values[0])
                if (game["h_score"].values[0] < game["a_score"].values[0]):
                    if (i == 0):
                        gameStats.append(3)
                        gameStats.append(1)
                        gameStats.append(0)
                        gameStats.append(0)
                    else:
                        gameStats.append(stats[-1][2] + 3)
                        gameStats.append(stats[-1][3] + 1)
                        gameStats.append(stats[-1][4])
                        gameStats.append(stats[-1][5])
                elif (game["h_score"].values[0] == game["a_score"].values[0]):
                    if (i == 0):
                        gameStats.append(1)
                        gameStats.append(0)
                        gameStats.append(1)
                        gameStats.append(0)
                    else:
                        gameStats.append(stats[-1][2] + 1)
                        gameStats.append(stats[-1][3])
                        gameStats.append(stats[-1][4] + 1)
                        gameStats.append(stats[-1][5])
                else:
                    if (i == 0):
                        gameStats.append(0)
                        gameStats.append(0)
                        gameStats.append(0)
                        gameStats.append(1)
                    else:
                        gameStats.append(stats[-1][2])
                        gameStats.append(stats[-1][3])
                        gameStats.append(stats[-1][4])
                        gameStats.append(stats[-1][5] + 1)
                if (i == 0):
                    gameStats.append(game["a_score"].values[0])
                    gameStats.append(game["h_score"].values[0])
                    gameStats.append(gameStats[-2] - gameStats[-1])
                else:
                    gameStats.append(stats[-1][6] + game["a_score"].values[0])
                    gameStats.append(stats[-1][7] + game["h_score"].values[0])
                    gameStats.append(gameStats[-2] - gameStats[-1])
                gameStats.append(int(i+1))
                # print(gameStats)
                stats.append(gameStats)
        else:
            if (i == 0):
                gameStats.append()
            else:
                gameStats = stats[-1].copy()
                gameStats[-1] = i+1
                stats.append(gameStats)
    # print(len(stats))
    return stats

def getPlacesOverTime(df):
    teams = pd.unique(df[["homeTeam", "awayTeam"]].values.ravel())
    teamsLeaderboardStatsOverGames = []
    for team in teams:
        # print(team)
        teamsLeaderboardStatsOverGames.append(getStatsOverGames(df, team))
        # print("\n")
    return teamsLeaderboardStatsOverGames

if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
# for i in range(10):
for i in range(nbYearToGet):
    print("Getting data for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    matchs = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/Match.csv")
    # print(matchs.head())
    datas = getPlacesOverTime(matchs)
    newDatas = []
    nbMatchs = []
    for data in datas:
        nbMatchs.append(len(data))
        for teamStats in data:
            newDatas.append(teamStats)
    pdDatas = pd.DataFrame(np.asarray(newDatas), columns=["id", "abbr", "points", "wins", "draws", "loses", "goalsFor", "goalsAgainst", "goalsDiff", "leagueMatchNb"])
    # print(pdDatas.loc[""])
    # print(pdDatas)
    leaderBoard = []
    for n in range(min(nbMatchs)):
        # print(i+1)
        standing = (pdDatas.loc[pdDatas["leagueMatchNb"] == str(n+1)]).sort_values(by=["points", "goalsDiff", "goalsFor"], ascending=False)
        tmp = []
        tmp.append(n+1)
        for team in standing["abbr"].values:
            tmp.append(team)
        leaderBoard.append(tmp)
        # print()
    # print(leaderBoard)
    pd.DataFrame(np.asarray(leaderBoard)).to_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/Leaderboard.csv", header=["id", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th"], index=None)
    print("   Leaderboard saved: " + str(int(year)-i)+"-"+str(int(year)-i+1)+"/Leaderboard.csv\n")

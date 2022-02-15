import pandas as pd
import numpy as np
import sys
import time
from datetime import date

if (len(sys.argv) == 3):
    year = int(str(sys.argv[2]))
else:
    year = date.today().strftime("%Y")
arg = int(str(sys.argv[1]))
nbYearToGet = int(year) - arg + 1
names = []
for i in range(nbYearToGet):
    print("Getting teams for year: " + str(int(year)-i) + "-" + str(int(year)-i+1))
    df = pd.read_csv(str(int(year)-i)+"-"+str(int(year)-i+1)+"/raw_standing.csv")
    teams = df.iloc[[0]].to_numpy()[0][1:]
    for team in teams:
        if team not in names:
            names.append(team)
# print(len(names))
print()
for team in names:
    print(team)

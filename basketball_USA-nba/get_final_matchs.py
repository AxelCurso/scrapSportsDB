import sys
import pandas as pd

def changeDates(dates):
    newDates = []
    months = {"January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"}
    for d in dates:
        splt = d.split(' ')
        newDates.append(int(splt[2]+months[splt[0]]+"{:02d}".format(int(splt[1].split(',')[0]))))
    return newDates

if (len(sys.argv) != 2):
    print("USAGE: python3 get_final_matchs.py $YEAR")
    exit()
year = sys.argv[1]
df = pd.read_csv(str(year)+"/raw_matchs.csv")
dates = df["date"]
newDates = changeDates(dates)
df["date"] = newDates
df.to_csv(str(year)+"/final_matchs.csv", index=None)

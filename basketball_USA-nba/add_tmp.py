import pandas as pd
import sys
import os

if (len(sys.argv) != 2):
    print("USAGE: python3 add_tmp.py $YEAR")
    exit()
year = sys.argv[1]
header =    [
            "id", "date", "homeTeam", "awayTeam", "h_score", "a_score", "lc", "tc",
            "h_q1", "h_q2", "h_q3", "h_q4", "h_pitp", "h_fbpts", "h_bigld", "h_benchpts", "h_tmreb", "h_tov", "h_tmtov", "h_ptsofto",
            "a_q1", "a_q2", "a_q3", "a_q4", "a_pitp", "a_fbpts", "a_bigld", "a_benchpts", "a_tmreb", "a_tov", "a_tmtov", "a_ptsofto",
            "h_fga", "h_fgp", "h_3pa", "h_3pp", "h_fta", "h_ftp", "h_oreb", "h_dreb", "h_ast", "h_stl", "h_blk", "h_to", "h_pf",
            "a_fga", "a_fgp", "a_3pa", "a_3pp", "a_fta", "a_ftp", "a_oreb", "a_dreb", "a_ast", "a_stl", "a_blk", "a_to", "a_pf",
            "h_sa", "h_sap", "h_dfl", "h_olbr", "h_dlbr", "h_c2s", "h_c3s", "h_obo", "h_dbo",
            "a_sa", "a_sap", "a_dfl", "a_olbr", "a_dlbr", "a_c2s", "a_c3s", "a_obo", "a_dbo"
            ]
tmp = pd.read_csv("tmp_raw_matchs.csv")
old = pd.read_csv(str(year)+"/raw_matchs.csv")
df = pd.concat([old,tmp])
df.drop_duplicates(inplace=True)
df.to_csv(str(year)+"/raw_matchs.csv", header=header, index=None)
os.system("python3 get_final_matchs.py "+str(year))

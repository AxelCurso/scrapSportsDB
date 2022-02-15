#!/bin/zsh

if [ $# -eq 2 ] ; then
	python3 get_raw_standings.py $1 $2
    python3 get_raw_matchs.py $1 $2
    python3 change_for_good_abbr.py $1 $2
else
    echo "Usage: ./all_in_one.sh FIRST_YEAR SECOND_YEAR"
fi

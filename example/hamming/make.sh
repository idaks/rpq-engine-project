#!/usr/bin/env bash

# set variables
source ../settings.sh

PATH_TO_DB="./"
DB_NAME="hamming.db"

mkdir -p $RESULTS_DIR
# generate the hamming dataset with numbers less than 1000 to hamming.db
sqlite3 "$PATH_TO_DB/$DB_NAME" < "$PATH_TO_DB/hamming_generator.sql"

# run rpq3 query "2.3.5" on hamming fish
QUERY1="2.3.5"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" fish -c $QUERY1 > "$RESULTS_DIR/QueryFish_235.txt"
# run rpq3 query "2.3.5" on hamming fish
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" sail -c $QUERY1 > "$RESULTS_DIR/QuerySail_235.txt"

# run rpq3 query "(5.2)+" on hamming fish
QUERY2="(5.2)+"
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" fish -c $QUERY2 > "$RESULTS_DIR/QueryFish_52+.txt"
# run rpq3 query "(5.2)+" on hamming fish
python ../../query_compiler.py "$PATH_TO_DB/$DB_NAME" sail -c $QUERY2 > "$RESULTS_DIR/QuerySail_52+.txt"

PATH_TO_DB="./"
HAMMING_DB_NAME="hamming.db"

# generate the hamming dataset with numbers less than 1000 to hamming.db
sqlite3 "$PATH_TO_DB/$HAMMING_DB_NAME" < "$PATH_TO_DB/hamming_generator.sql"

# run rpq3 query "2.3.5" on hamming fish
QUERY1="2.3.5"
python ../../query_compiler.py "$PATH_TO_DB/$HAMMING_DB_NAME" fish -c $QUERY1 > "QueryFish1.txt"
# run rpq3 query "2.3.5" on hamming fish
python ../../query_compiler.py "$PATH_TO_DB/$HAMMING_DB_NAME" sail -c $QUERY1 > "QuerySail1.txt"

# run rpq3 query "(5.2)+" on hamming fish
QUERY2="(5.2)+"
python ../../query_compiler.py "$PATH_TO_DB/$HAMMING_DB_NAME" fish -c $QUERY2 > "QueryFish2.txt"
# run rpq3 query "(5.2)+" on hamming fish
python ../../query_compiler.py "$PATH_TO_DB/$HAMMING_DB_NAME" sail -c $QUERY2 > "QuerySail2.txt"

# generate the hamming dataset with numbers less than 1000 to hamming.db
sqlite3 hamming.db < hamming_generator.sql

# generate tables for fish and sail:
# tc2plus: a path from startNode to Endnode that consists edge label 2
# tc3plus: a path from startNode to Endnode that consists edge label 3
# tc5plus: a path from startNode to Endnode that consists edge label 5
sqlite3 hamming.db < tcrecursive.sql

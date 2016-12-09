import pandas as pd
import sqlite3

temp_num = 0

def get_star(prev,x):
    global temp_num
    if prev < 0:
        temp_table = "temp"+str(temp_num)
        parse =  '''
        {0}(start, end) AS (
            VALUES(1,1)
            UNION ALL
            SELECT {0}.start, fish.endNode FROM {0},fish 
            WHERE {0}.end = fish.startNode AND fish.label = {1} 
        )
    '''.format(temp_table,x)
        temp_num += 1
    else:
        temp_table = "temp"+str(temp_num)
        prev_table = "temp"+str(prev)
        parse = '''
        {1}(start, end) AS (
            SELECT * FROM {2}
            UNION ALL
            SELECT {1}.start, fish.endNode FROM {1},fish 
            WHERE {1}.end = fish.startNode AND fish.label = {0} 
        )
        '''.format(x,temp_table,prev_table)
        temp_num += 1

    return parse
if __name__ == "__main__":
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("hamming.db")
    
    # '2*3*'->'2*''3*'
    x = '2'
    y = '3'

    with_rec ='WITH RECURSIVE '
    temp0 = get_star(-1,x)
    temp1 = get_star(0,y)
    sql_str = with_rec + temp0 + ","+temp1 + " select * from temp1;"
    print(sql_str)
    df = pd.read_sql_query("sql_str", con)

    con.close()


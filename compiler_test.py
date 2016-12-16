import pandas as pd
import sqlite3

temp_num = 0
temp_table_dict = {} 
def conc_table_with_comma():
    '''
        concatenate all temp tables inside the "WITH RECURSIVE" with comma
    '''
    if(temp_num > 0):
        rtn = temp_table_dict[1]
        for i in range(2,temp_num+1):
            rtn += ","+temp_table_dict[i]
    else:
        return None
    return rtn

def literal(literal):
    '''
        form the data with edge label literal into a temp table
        input: char
        output: tuple(temp table idx, SQL string)
    '''

    global temp_num
    temp_num += 1
    temp_table = "temp"+str(temp_num)
    parse =  '''
    {0}(start, end) AS (
        SELECT fish.startNode,fish.endNode FROM fish 
        WHERE fish.label = {1}
    )
    '''.format(temp_table,literal)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn


def OR(leftChild, rightChild):
    '''
        input: 
            leftChild: temp table idx
            rightChild: temp table idx
        output: tuple(temp table idx, SQL string)
    '''

    global temp_num
    temp_num += 1
    temp_table = "temp"+str(temp_num)
    leftChild_table = "temp"+str(leftChild)
    rightChild_table = "temp"+str(rightChild)
    parse =  '''
    {0}(start, end) AS (
        SELECT * FROM {1}
        UNION ALL
        SELECT * FROM {2}
    )
    '''.format(temp_table,leftChild_table, rightChild_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn

def CONC(leftChild, rightChild):
    '''
        input: 
            leftChild: temp table idx
            rightChild: temp table idx
        output: tuple(temp table idx, SQL string)
    '''
    global temp_num
    temp_num += 1
    temp_table = "temp"+str(temp_num)
    leftChild_table = "temp"+str(leftChild)
    rightChild_table = "temp"+str(rightChild)
    parse =  '''
    {0}(start, end) AS (
        SELECT {1}.start, {2}.end FROM {1},{2} 
        WHERE {1}.end = {2}.start
    )
    '''.format(temp_table,leftChild_table, rightChild_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

def STAR(child):
    '''
        input: 
            child: temp table idx
        output: tuple(temp table idx, SQL string)
    '''
    global temp_num
    temp_num += 1
    temp_table = "temp"+str(temp_num)
    child_table = "temp"+str(child)
    parse =  '''
        {0}(start, end) AS (
            SELECT * FROM {1}
            UNION ALL
            SELECT {0}.start, {1}.end FROM {0},{1} 
            WHERE {0}.end = {1}.start
        )
    '''.format(temp_table,child_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

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

def test0(con):
    # 2
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(2)
    sql_str = "{}  {}  select * from temp{};".format(with_rec, temp0, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)
    
def test1(con):
    # 5.2 
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(2)
    (idx2, temp2) = CONC(idx0,idx1);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

def test2(con):
    # 532|2355 
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(3)
    # 5.3
    (idx2, temp2) = CONC(idx0,idx1);
    (idx3, temp3) = literal(2)
    # 5.3.2
    (idx4, temp4) = CONC(idx2,idx3);
    # 2.3
    (idx5, temp5) = CONC(idx3,idx1);
    # 2.3.5
    (idx6, temp6) = CONC(idx5,idx0);
    # 2.3.5.5
    (idx7, temp7) = CONC(idx6,idx0);
    (idx8, temp8) = OR(idx4,idx7);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

def test3(con):
    # (5.2)* 
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(2)
    (idx2, temp2) = CONC(idx0,idx1);
    (idx3, temp3) = STAR(idx2);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)
'''
def prevtest(con):
    # '2*3*'->'2*''3*'
    x = '2'
    y = '3'

    with_rec ='WITH RECURSIVE '
    temp0 = get_star(-1,x)
    temp1 = get_star(0,y)
    sql_str = "{} {}, {}  select * from temp{};".format(with_rec, temp0,temp1, temp_num-1);
    #sql_str = with_rec + temp0 + ","+temp1 + " select * from temp1;"
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)
   '''

if __name__ == "__main__":
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("data/hamming.db")
    test3(con)
    
    con.close()


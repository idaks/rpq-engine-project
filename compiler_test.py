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
        UNION
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
            SELECT fish.startNode,fish.startNode FROM fish 
            UNION 
            SELECT fish.endNode,fish.endNode FROM fish 
            UNION
            SELECT {0}.start, {1}.end FROM {0},{1} 
            WHERE {0}.end = {1}.start
        )
    '''.format(temp_table,child_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

def PLUS(child):
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
            UNION
            SELECT {0}.start, {1}.end FROM {0},{1} 
            WHERE {0}.end = {1}.start
        )
    '''.format(temp_table,child_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

def MINUS(child):
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
            SELECT {1}.end, {1}.start FROM {1} 
        )
    '''.format(temp_table,child_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

def OPTIONAL(child):
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
            SELECT fish.startNode,fish.startNode FROM fish 
            UNION 
            SELECT fish.endNode,fish.endNode FROM fish 
            UNION
            SELECT * FROM {1}
        )
    '''.format(temp_table,child_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

def test0(con):
    # 2
    print("2")
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(2)
    sql_str = "{}  {}  select * from temp{};".format(with_rec, temp0, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)
    
def test1(con):
    # 5.2 
    print("5.2")
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
    print("532|2355")
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
    # 5* 
    print("3*")
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(3)
    (idx1, temp1) = STAR(idx0);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

def test4(con):
    # (5.2)* 
    print("(5.2)*")
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

def test5(con):
    # 5(52)*3* 
    print("5(52)*3*")
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(2)
    (idx2, temp2) = CONC(idx0,idx1);
    (idx3, temp3) = STAR(idx2);
    (idx4, temp4) = CONC(idx0,idx3);
    (idx5, temp5) = literal(3)
    (idx6, temp6) = STAR(idx4);
    (idx7, temp7) = CONC(idx4,idx6);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

def test6(con):
    # (52)+3+ 
    print("(52)+3+")
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(2)
    (idx2, temp2) = CONC(idx0,idx1);
    (idx3, temp3) = PLUS(idx2);
    (idx4, temp4) = literal(3)
    (idx5, temp5) = PLUS(idx4);
    (idx6, temp6) = CONC(idx3,idx5);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

def test7(con):
    # (5(52)*3*)- 
    print("(5(52)*3*)-")
    with_rec ='WITH RECURSIVE '
    (idx0, temp0) = literal(5)
    (idx1, temp1) = literal(2)
    (idx2, temp2) = CONC(idx0,idx1);
    (idx3, temp3) = STAR(idx2);
    (idx4, temp4) = CONC(idx0,idx3);
    (idx5, temp5) = literal(3)
    (idx6, temp6) = STAR(idx4);
    (idx7, temp7) = CONC(idx4,idx6);
    (idx8, temp8) = MINUS(idx7);
    tables = conc_table_with_comma()
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    print(sql_str)
    df = pd.read_sql_query(sql_str, con)
    print(df)

if __name__ == "__main__":
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("data/hamming.db")
    test5(con)
    
    con.close()


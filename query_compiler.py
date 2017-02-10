import sys
import pandas as pd
import sqlite3
import yacc
import lex
dict_val_idx = {}
dict_idx_sql = {}
temp_num = 0
temp_table_dict = {} 
def sql_generation():
    '''
        concatenate string that will be paesed into sql 
    '''
    with_rec ='WITH RECURSIVE '
    if(temp_num > 0):
        tables = temp_table_dict[1]
        for i in range(2,temp_num+1):
            tables += ","+temp_table_dict[i]
    else:
        return None
    sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, temp_num);
    return sql_str

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
        SELECT {2}.startNode,{2}.endNode FROM {2}
        WHERE {2}.label = {1}
    )
    '''.format(temp_table,literal,target_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    dict_val_idx[literal] = temp_num
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
        SELECT a.start, b.end FROM {1} AS a,{2} AS b
        WHERE a.end = b.start
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
            SELECT {2}.startNode,{2}.startNode FROM {2}
            UNION 
            SELECT {2}.endNode,{2}.endNode FROM {2}
            UNION
            SELECT a.start, b.end FROM {0} AS a,{1} AS b
            WHERE a.end = b.start
        )
    '''.format(temp_table,child_table, target_table)
    temp_table_dict[temp_num] = parse
    rtn =  (temp_num,parse);
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
            SELECT a.start, b.end FROM {0} AS a,{1} AS b
            WHERE a.end = b.start
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

def QMARK(child):
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
            SELECT {2}.startNode,{2}.startNode FROM {2}
            UNION 
            SELECT {2}.endNode,{2}.endNode FROM {2}
            UNION
            SELECT * FROM {1}
        )
    '''.format(temp_table,child_table,target_table)
    rtn =  (temp_num,parse);
    temp_table_dict[temp_num] = parse
    return rtn;

class Parser:

    tokens = ()
    precedence = ()
    
    def __init__(self, arg1):
        lexer = lex.lex(module = self)

        # Build the parser
        yacc.yacc(module=self)

    def run(self, data):
        # Parse.
        yacc.parse(data)
    
    def printList(self):
        pass

class queryParser(Parser):
    # List of token names.   This is always required
    tokens = ('EDGEID','LPAREN','RPAREN','OR','CONC','STAR', 'PLUS', 'MINUS', 'QMARK')

# Regular expression rules for simple tokens
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_CONC = r'\.'
    t_OR = r'\|'
    t_STAR = r'\*'
    t_EDGEID = r'[a-zA-Z0-9_][a-zA-Z0-9_]*'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_QMARK = r'\?'
 
# Define a rule so we can track line numbers
    def t_newline(self, t):
            r'\n+'
            t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

# Error handling rule
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

# Parsing Expressions
    precedence = ( ('left', 'OR'), ('left', 'CONC'), ('left','STAR','PLUS', 'MINUS', 'QMARK'))

    def p_expressions_edge(self, t):
        '''expression    : EDGEID'''
        t[0] = t[1]
        if t[0] not in dict_val_idx:
            literal(t[0])
            dict_val_idx[t[0]] = temp_num
    
    def p_expression_single(self, t):
        '''expression    : LPAREN expression RPAREN'''
        t[0] = "(" + t[2] + ")"
        dict_val_idx[t[0]] = dict_val_idx[t[2]]

    def p_expression_recursiveBinary(self, t):
        '''expression    : expression OR expression
                | expression CONC expression'''
        if (t[2] == '|'):
            print("Recursive Or")
            t[0] = t[1] + "|" + t[3]
            if t[0] not in dict_val_idx:
                leftChild = dict_val_idx[t[1]]
                rightChild = dict_val_idx[t[3]]
                OR(leftChild, rightChild)
                dict_val_idx[t[0]] = temp_num
        else:
            print("Recursive Conc")
            t[0] = t[1] + "." + t[3]
            if t[0] not in dict_val_idx:
                leftChild = dict_val_idx[t[1]]
                rightChild = dict_val_idx[t[3]]
                CONC(leftChild, rightChild)
                dict_val_idx[t[0]] = temp_num

    def p_expression_starEdge(self, t):
        '''expression    : expression STAR'''
        print("Star on edge")
        t[0] = t[1] + "*"
        if t[0] not in dict_val_idx:
            child = dict_val_idx[t[1]]
            STAR(child)
            dict_val_idx[t[0]] = temp_num

    def p_expression_plusEdge(self, t):
        '''expression    : expression PLUS'''
        print("Plus on edge")
        t[0] = t[1] + "+"
        if t[0] not in dict_val_idx:
            child = dict_val_idx[t[1]]
            PLUS(child)
            dict_val_idx[t[0]] = temp_num

    def p_expression_minusEdge(self, t):
        '''expression    : expression MINUS'''
        print("Minus on edge")
        t[0] = t[1] + "-"
        if t[0] not in dict_val_idx:
            child = dict_val_idx[t[1]]
            MINUS(child)
            dict_val_idx[t[0]] = temp_num

    def p_expression_qmarkEdge(self, t):
        '''expression    : expression QMARK'''
        print("Optional on edge")
        t[0] = t[1] + "?"
        if t[0] not in dict_val_idx:
            child = dict_val_idx[t[1]]
            QMARK(child)
            dict_val_idx[t[0]] = temp_num

    def p_expression_expression(self, t):
        '''expression    : expression expression'''
        print("Concatenate two expressions")
        t[0] = t[1] + "." + t[2]
        if t[0] not in dict_val_idx:
            leftChild = dict_val_idx[t[1]]
            rightChild = dict_val_idx[t[2]]
            CONC(leftChild, rightChild)
            dict_val_idx[t[0]] = temp_num

    def p_error(self, p):
            if p:
                print("Syntax error at '%s'" % p.value)
            else:
                print("Syntax error at EOF")

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("Usage: python query_compiler.py (database) (table)")
        exit()
    global target_table            
    # Read sqlite query results into a pandas DataFrame
    path = sys.argv[1]
    target_table = sys.argv[2]
    # "data/hamming.db"
    con = sqlite3.connect(path)
    
    while 1:
        try:
            s = raw_input('rpq > ')
        except EOFError:
            break
        if not s:
            continue
        print('Query: {}\nParsing...\n'.format(s))
        calc = queryParser(True)
        calc.run(s)
        sql_str = sql_generation()
        # print(sql_str)
        try:
            df = pd.read_sql_query(sql_str, con)
            pd.set_option('display.max_rows', len(df))
            print(df)
        except:
            print("Query Failed!")

    con.close()

import sys
import pandas as pd
import sqlite3
import yacc
import lex

class sql_compiler:
    def __init__(self):
        self.dict_val_idx = {}
        self.dict_idx_sql = {}
        self.temp_num = 0

    def sql_generation(self):
        '''
            concatenate string that will be paesed into sql 
        '''
        with_rec ='WITH RECURSIVE '
        if(self.temp_num > 0):
            tables = self.dict_idx_sql[1]
            for i in range(2,self.temp_num+1):
                tables += ","+self.dict_idx_sql[i]
        else:
            return None
        sql_str = "{}  {}  select * from temp{};".format(with_rec, tables, self.temp_num);
        print(sql_str)
        return sql_str

    def node(self, node):
        '''
            input: 
                node: node name
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        parse =  '''
        {0}(start, end) AS (
            SELECT a.startNode, a.startNode FROM {1} AS a
            WHERE a.startNode = {2}
            UNION
            SELECT a.endNode, a.endNode FROM {1} AS a
            WHERE a.endNode = {2}
        )
        '''.format(temp_table, target_table, node)
        return parse

    def label(self, label):
        #TODO: Maybe need quotation
        '''
            form the data with edge label into a temp table
            input: char
            output: SQL string)
        '''

        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        parse =  '''
        {0}(start, end) AS (
            SELECT {2}.startNode,{2}.endNode FROM {2}
            WHERE {2}.label = {1}
        )
        '''.format(temp_table,label,target_table)
        return parse


    def OR(self, leftChild, rightChild):
        '''
            input: 
                leftChild: temp table idx
                rightChild: temp table idx
            output: SQL string)
        '''

        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        leftChild_table = "temp"+str(leftChild)
        rightChild_table = "temp"+str(rightChild)
        parse =  '''
        {0}(start, end) AS (
            SELECT * FROM {1}
            UNION
            SELECT * FROM {2}
        )
        '''.format(temp_table,leftChild_table, rightChild_table)
        return parse

    def CONC(self, leftChild, rightChild):
        '''
            input: 
                leftChild: temp table idx
                rightChild: temp table idx
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        leftChild_table = "temp"+str(leftChild)
        rightChild_table = "temp"+str(rightChild)
        parse =  '''
        {0}(start, end) AS (
            SELECT a.start, b.end FROM {1} AS a,{2} AS b
            WHERE a.end = b.start
        )
        '''.format(temp_table,leftChild_table, rightChild_table)
        return parse

    def STAR(self, child):
        '''
            input: 
                child: temp table idx
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
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
        return parse

    def PLUS(self, child):
        '''
            input: 
                child: temp table idx
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        child_table = "temp"+str(child)
        parse =  '''
            {0}(start, end) AS (
                SELECT * FROM {1}
                UNION
                SELECT a.start, b.end FROM {0} AS a,{1} AS b
                WHERE a.end = b.start
            )
        '''.format(temp_table,child_table)
        return parse

    def MINUS(self,child):
        '''
            input: 
                child: temp table idx
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        child_table = "temp"+str(child)
        parse =  '''
            {0}(start, end) AS (
                SELECT {1}.end, {1}.start FROM {1} 
            )
        '''.format(temp_table,child_table)
        return parse

    def QMARK(self, child):
        '''
            input: 
                child: temp table idx
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
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
        return parse

class Parser:

    tokens = ()
    precedence = ()
    
    def __init__(self):
        print("init parser")
        self.sql = sql_compiler()
        lexer = lex.lex(module = self)

        # Build the parser
        yacc.yacc(module=self)

    def run(self, data):
        # Parse.
        print(self.sql.dict_val_idx, self.sql.dict_idx_sql, self.sql.temp_num)
        yacc.parse(data)
    
    def printList(self):
        pass

class queryParser(Parser):
    # List of token names.   This is always required
    tokens = ('NODEID', 'EDGEID','LPAREN','RPAREN','OR','CONC','STAR', 'PLUS', 'MINUS', 'QMARK')

# Regular expression rules for simple tokens
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_CONC = r'\.'
    t_OR = r'\|'
    t_STAR = r'\*'
    t_NODEID= r'\[[a-zA-Z0-9_][a-zA-Z0-9_]*\]'
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

    def p_expression_node(self, t):
        ''' expression    : NODEID '''
        print("Node")
        t[0] = t[1]
        if t[0] not in self.sql.dict_val_idx:
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.node(t[0][1:-1])
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expressions_edge(self, t):
        '''expression    : EDGEID'''
        print("Edge")
        t[0] = t[1]
        if t[0] not in self.sql.dict_val_idx:
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.label(t[0])
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num
        print(self.sql.dict_val_idx)
    
    def p_expression_single(self, t):
        '''expression    : LPAREN expression RPAREN'''
        print("()")
        t[0] = "(" + t[2] + ")"
        self.sql.dict_val_idx[t[0]] = self.sql.dict_val_idx[t[2]]

    def p_expression_recursiveBinary(self, t):
        '''expression    : expression OR expression
                | expression CONC expression'''
        if (t[2] == '|'):
            print("Recursive Or")
            t[0] = t[1] + "|" + t[3]
            if t[0] not in dict_val_idx:
                leftChild = self.sql.dict_val_idx[t[1]]
                rightChild = self.sql.dict_val_idx[t[3]]
                self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.OR(leftChild, rightChild)
                self.sql.dict_val_idx[t[0]] = self.sql.temp_num
        else:
            print("Recursive Conc")
            t[0] = t[1] + "." + t[3]
            if t[0] not in self.sql.dict_val_idx:
                leftChild = self.sql.dict_val_idx[t[1]]
                rightChild = self.sql.dict_val_idx[t[3]]
                self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.CONC(leftChild, rightChild)
                self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_starEdge(self, t):
        '''expression    : expression STAR'''
        print("Star on edge")
        t[0] = t[1] + "*"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.STAR(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_plusEdge(self, t):
        '''expression    : expression PLUS'''
        print("Plus on edge")
        t[0] = t[1] + "+"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.PLUS(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_minusEdge(self, t):
        '''expression    : expression MINUS'''
        print("Minus on edge")
        t[0] = t[1] + "-"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.MINUS(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_qmarkEdge(self, t):
        '''expression    : expression QMARK'''
        print("Optional on edge")
        t[0] = t[1] + "?"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.QMARK(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_expression(self, t):
        '''expression    : expression expression'''
        print("Concatenate two expressions")
        t[0] = t[1] + "." + t[2]
        if t[0] not in self.sql.dict_val_idx:
            leftChild = self.sql.dict_val_idx[t[1]]
            rightChild = self.sql.dict_val_idx[t[2]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.CONC(leftChild, rightChild)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

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
        calc = queryParser()
        calc.run(s)
        sql_str = calc.sql.sql_generation()
        # print(sql_str)
        try:
            df = pd.read_sql_query(sql_str, con)
            pd.set_option('display.max_rows', len(df))
            print(df)
        except:
            print("Query Failed!")

    con.close()

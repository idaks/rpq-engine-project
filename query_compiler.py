import sys
import pandas as pd
import sqlite3
import yacc
import lex
import argparse

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
        if debug:
            print(sql_str)
        return sql_str

    def node(self, node):
        '''
            input: 
                node: node name
            output: SQL string)
        '''
        if isinstance(node, str): 
            node_with_type = "\""+node+"\""
        else:
            # TODO: possibly add more type check
            node_with_type = node
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        if "-5" in sys.argv:
            parse =  '''
            {0}(start, end, inter_start, label, inter_end) AS (
                SELECT a.startNode, a.startNode, 
                a.startNode, "node_self" AS label, a.startNode 
                FROM {1} AS a
                WHERE a.startNode = {2}
                UNION
                SELECT a.endNode, a.endNode,  
                a.endNode, "node_self" AS label, a.endNode 
                FROM {1} AS a
                WHERE a.endNode = {2}
            )
            '''.format(temp_table, target_table, node_with_type)
        else:
            parse =  '''
            {0}(start, end) AS (
                SELECT a.startNode, a.startNode FROM {1} AS a
                WHERE a.startNode = {2}
                UNION
                SELECT a.endNode, a.endNode FROM {1} AS a
                WHERE a.endNode = {2}
            )
            '''.format(temp_table, target_table, node_with_type)
        self.dict_idx_sql[self.temp_num] = parse
        return parse

    def label(self, label):
        #TODO: Maybe need quotation
        if isinstance(label, str): 
            label_with_type = "\""+label+"\""
        else:
            # TODO: possibly add more type check
            label_with_type = label
        '''
            form the data with edge label into a temp table
            input: char
            output: SQL string)
        '''
        self.temp_num += 1
        temp_table = "temp"+str(self.temp_num)
        if "-5" in sys.argv:
            parse =  '''
            {0}(start, end, inter_start, label, inter_end) AS (
                SELECT {2}.startNode,{2}.endNode, 
                {2}.startNode, {1} AS label, {2}.endNode 
                FROM {2}
                WHERE {2}.label = {1}
            )
            '''.format(temp_table,label_with_type,target_table)
        else:
            parse =  '''
            {0}(start, end) AS (
                SELECT {2}.startNode,{2}.endNode FROM {2}
                WHERE {2}.label = {1}
            )
            '''.format(temp_table,label_with_type,target_table)
        self.dict_idx_sql[self.temp_num] = parse
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
        if "-5" in sys.argv:
            parse =  '''
            {0}(start, end, inter_start, label, inter_end) AS (
                SELECT * FROM {1}
                UNION
                SELECT * FROM {2}
            )
            '''.format(temp_table,leftChild_table, rightChild_table)
        else:
            parse =  '''
            {0}(start, end) AS (
                SELECT * FROM {1}
                UNION
                SELECT * FROM {2}
            )
            '''.format(temp_table,leftChild_table, rightChild_table)
        self.dict_idx_sql[self.temp_num] = parse
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
        if "-5" in sys.argv:
            # rpq only with starting, and ending nodes
            rpq2 =  '''
            {0}(start, internal, end) AS (
                SELECT a.start, a.end, b.end  FROM {1} AS a,{2} AS b
                WHERE a.end = b.start
            )
            '''.format(temp_table,leftChild_table, rightChild_table)
            self.dict_idx_sql[self.temp_num] = rpq2 

            self.temp_num += 1
            temp_table2 = "temp"+str(self.temp_num)
            rpq4 =  '''
            {0}(start, end, inter_start, label, inter_end) AS (
                SELECT rpq2.start, rpq2.end, 
                a.inter_start, a.label, a.inter_end 
                FROM {1} AS rpq2, {2} AS a
                WHERE rpq2.internal = a.end AND rpq2.start = a.start
                UNION
                SELECT rpq2.start, rpq2.end, 
                b.inter_start, b.label, b.inter_end 
                FROM {1} AS rpq2, {3} AS b
                WHERE rpq2.internal = b.start AND rpq2.end = b.end
            )
            '''.format(temp_table2, temp_table, leftChild_table, rightChild_table)
            self.dict_idx_sql[self.temp_num] = rpq4
            parse = '{}\n{}'.format(rpq2, rpq4)
        else:
            parse =  '''
            {0}(start, end) AS (
                SELECT a.start, b.end FROM {1} AS a,{2} AS b
                WHERE a.end = b.start
            )
            '''.format(temp_table,leftChild_table, rightChild_table)
            self.dict_idx_sql[self.temp_num] = parse
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
        if "-5" in sys.argv:
            rpq2 =  '''
                {0}(start, internal, end) AS (
                    SELECT {2}.startNode,NULL, {2}.startNode 
                    FROM {2}
                    UNION 
                    SELECT {2}.endNode,NULL, {2}.endNode 
                    FROM {2}
                    UNION
                    SELECT a.start, a.end, b.end FROM {0} AS a,{1} AS b
                    WHERE a.end = b.start
                )
            '''.format(temp_table,child_table, target_table)
            self.dict_idx_sql[self.temp_num] = rpq2
            
            self.temp_num += 1
            temp_table2 = "temp"+str(self.temp_num)
            rpq5 =  '''
                {0}(start, end, inter_start, label, inter_end) AS (
                    SELECT {3}.startNode,{3}.startNode, 
                    {3}.startNode, "empty_star" AS label, {3}.startNode
                    FROM {3}
                    UNION 
                    SELECT {3}.endNode,{3}.endNode, 
                    {3}.endNode, "empty_star" AS label, {3}.endNode
                    FROM {3}
                    UNION
                    SELECT a.start, a.end,
                    b.inter_start, b.label, b.inter_end
                    FROM {1} AS a,{2} AS b
                    WHERE a.internal = b.start
                )
            '''.format(temp_table2, temp_table, child_table, target_table)
            self.dict_idx_sql[self.temp_num] = rpq5
            parse = "{}\n{}".format(rpq2, rpq5)
        else:
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
            self.dict_idx_sql[self.temp_num] = parse
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
        if "-5" in sys.argv:
            pass
        else:
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
        if "-5" in sys.argv:
            pass
        else:
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
        if "-5" in sys.argv:
            pass
        else:
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
        if debug:
            print("init parser")
        self.sql = sql_compiler()
        lexer = lex.lex(module = self)

        # Build the parser
        yacc.yacc(module=self)

    def run(self, data):
        # Parse.
        if debug:
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
        t[0] = t[1]
        if t[0] not in self.sql.dict_val_idx:
            self.sql.node(t[0][1:-1])
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num
        if debug:
            print("Node")
            print(self.sql.dict_val_idx)

    def p_expressions_edge(self, t):
        '''expression    : EDGEID'''
        t[0] = t[1]
        if t[0] not in self.sql.dict_val_idx:
            self.sql.label(t[0])
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num
        if debug:
            print("Edge")
            print(self.sql.dict_val_idx)
    
    def p_expression_single(self, t):
        '''expression    : LPAREN expression RPAREN'''
        if debug:
            print("()")
        t[0] = "(" + t[2] + ")"
        self.sql.dict_val_idx[t[0]] = self.sql.dict_val_idx[t[2]]

    def p_expression_recursiveBinary(self, t):
        '''expression    : expression OR expression
                | expression CONC expression'''
        if (t[2] == '|'):
            if debug:
                print("Recursive Or")
            t[0] = t[1] + "|" + t[3]
            if t[0] not in self.sql.dict_val_idx:
                leftChild = self.sql.dict_val_idx[t[1]]
                rightChild = self.sql.dict_val_idx[t[3]]
                self.sql.OR(leftChild, rightChild)
                self.sql.dict_val_idx[t[0]] = self.sql.temp_num
        else:
            if debug:
                print("Recursive Conc")
            t[0] = t[1] + "." + t[3]
            if t[0] not in self.sql.dict_val_idx:
                leftChild = self.sql.dict_val_idx[t[1]]
                rightChild = self.sql.dict_val_idx[t[3]]
                self.sql.CONC(leftChild, rightChild)
                self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_starEdge(self, t):
        '''expression    : expression STAR'''
        if debug:
            print("Star on edge")
        t[0] = t[1] + "*"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.STAR(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_plusEdge(self, t):
        '''expression    : expression PLUS'''
        if debug:
            print("Plus on edge")
        t[0] = t[1] + "+"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.PLUS(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_minusEdge(self, t):
        '''expression    : expression MINUS'''
        if debug:
            print("Minus on edge")
        t[0] = t[1] + "-"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.MINUS(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_qmarkEdge(self, t):
        '''expression    : expression QMARK'''
        if debug:
            print("Optional on edge")
        t[0] = t[1] + "?"
        if t[0] not in self.sql.dict_val_idx:
            child = self.sql.dict_val_idx[t[1]]
            self.sql.dict_idx_sql[self.sql.temp_num] = self.sql.QMARK(child)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_expression_expression(self, t):
        '''expression    : expression expression'''
        if debug:
            print("Concatenate two expressions")
        t[0] = t[1] + "." + t[2]
        if t[0] not in self.sql.dict_val_idx:
            leftChild = self.sql.dict_val_idx[t[1]]
            rightChild = self.sql.dict_val_idx[t[2]]
            self.sql.CONC(leftChild, rightChild)
            self.sql.dict_val_idx[t[0]] = self.sql.temp_num

    def p_error(self, p):
            if p:
                print("Syntax error at '%s'" % p.value)
            else:
                print("Syntax error at EOF")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Regular Path Query Engine')
    parser.add_argument('database', help='SQL Database to query')
    parser.add_argument('table', help='Table name in the database')
    parser.add_argument('-debug', action='store_true', help='Debug Mode')
    parser.add_argument('-c', nargs='+', help='command line mode')
    args = parser.parse_args()

    global target_table            
    global debug 
    # Read sqlite query results into a pandas DataFrame
    path = args.database
    target_table = args.table

    # debug mode
    if args.debug:
        debug = 1
    else:
        debug = 0
    con = sqlite3.connect(path)
    
    if not args.c:
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
            try:
                df = pd.read_sql_query(sql_str, con)
                pd.set_option('display.max_rows', len(df))
                print(df)
            except:
                print("Query Failed!")
    else:
        for c in args.c:
            print('Query: {}\nParsing...\n'.format(c))
            calc = queryParser()
            calc.run(c)
            sql_str = calc.sql.sql_generation()
            try:
                df = pd.read_sql_query(sql_str, con)
                pd.set_option('display.max_rows', len(df))
                print(df)
            except:
                print("Query Failed!")


    con.close()

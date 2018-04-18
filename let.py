# !/usr/bin/python

# Nicholas Gaston
# nigaston
# 2649642
""" interpreter for the following grammar:
<prog>       ::= <let-in-end> { <let-in-end> }
<let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;
<decl-list>  ::= <decl> { <decl> }
<decl>       ::= id : <type> = <expr> ;
<type>       ::= int | real
<expr>       ::= <term> { + <term> | - <term> }
<term>       ::= <factor> { * <factor> | / <factor> }
<factor>     ::= ( <expr> ) | id | number | <type> ( id )
"""

token = None
lines = []                                              # list of the words from the file
varmap = {}                                             # dict of the values of the variables
typemap = {}                                            # dict of the type of the variables
cursor = 0                                              # holds the postion in the file
i='int'
r='real'
#ansr = 0

def prog() :
    while token == 'let' :
        let_in_end()
        varmap.clear()
        typemap.clear()
    match('EOF')
    #prog()

def let_in_end() :
    ansr = 0                                            # holds the final value of the main expr

    #if token == 'let' :
    match('let')
    decl()

    #elif token == 'in' :
    match('in')
    if token == 'int' :
        match('int')
        if token == '(' :
            match('(')
            #print expr(i)
            ansr = expr(i)
            match(')')
        else :
            error()
    elif token == 'real' :
        match('real')
        if token == '(' :
            match('(')
            #print expr(r)
            ansr = expr(r)                              # pass the type 'real' to expr()
            match(')')
        else :
            error()
    else :
        error()

    #elif token == 'end' :
    match('end')
    #if token == ';' :
    match(';')
    print ansr                                         # PRINT VALUE OF EXPR
        # terminate
    #else :
        #error()

    #else :
        #error()

def decl() :
    if token != 'in' :
        v = token                                       # name of var
        match(token)
        #if token == ':' :
        match(':')
        if token == 'int' :
            match('int')
            typemap[v] = 'int'
            #if token == '=' :
            match('=')
            varmap[v] = int(expr(i))                # type cast to int, still pass 'int' for check
            #if token == ';' :
            match(';')
            decl()
                #else :
                    #error()
            #else :
                #error()
        elif token == 'real' :
            match('real')
            typemap[v] = 'real'
            #if token == '=' :
            match('=')
            varmap[v] = float(expr(r))              # type cast to float, still pass 'real' for check
            #if token == ';' :
            match(';')
            decl()
                #else :
                    #error()
            #else :
                #error()
        else :
            error()
        #else :
            #error()

def expr(t) :
    opp = term(t)
    #if token == '+' :
    while (token == '+') or (token == '-') :            # { + <term> | - <term> }
        if token == '+' :
            match('+')
            opp += term(t)
            #return opp
        elif token == '-' :
            match('-')
            opp -= term(t)
            #return opp
    #else:
    return opp

def term(t) :
    op1 = factor(t)
    while (token == '*') or (token == '/') :            # { * <factor> | / <factor> }
        if token == '*' :
            match('*')
            op1 *= factor(t)
            #return op1
        elif token == '/' :
            match('/')
            try :
                op1 /= factor(t)
            except ZeroDivisionError :
                error()
            #return op1
    #else:
    return op1

def factor(t) :
    if token == '(' :                                   # if ( <expr> )
        match('(')
        value = expr(t)
        match(')')
        return value
    elif token in varmap :                              # if id
        if t == typemap[token] :                        # type of id must match expected, t
            value = varmap[token]
            match(token)
            return value
        else :
            error()
    elif token.isdigit() or '.' in token :              # if number
        if (t == r) :
            for c in token :
                if (c.isdigit() == False) and c != '.' :
                    error()
            pcnt = token.count('.')
            if pcnt == 1 :                              # real can have one '.'
                value = float(token)
                match(token)
                return value
            else :
                error()
        elif  (t == i and token.isdigit()) :            # type of number must match expected, t
            value = int(token)
            match(token)
            return value
        else :
            error()
    elif token == 'int' :                               # if <int> ( id )
        match('int')
        #if t == 'int' :                                 # type of cast of id must match expected, t
            #if token == '(' :
        match('(')
        value = int(varmap[token])
        match(token)
        match(')')
        return value
        #else :
            #error()
    elif token == 'real' :                              # if <real> ( id )
        match('real')
        #if t == 'real' :                                # type of cast of id must match expected, t
            #if token == '(' :
        match('(')
        value = float(varmap[token])
        match(token)
        match(')')
        return value
        #else :
            #error()
    else:
        error()

""" def match()
: advances cursor if token matches parameter,
terminates if not
"""
def match(t) :
    if token == t:
        lex()
    else:
        error()

""" def error()
: prints error if called then aborts program
"""
def error() :
    print "Error"
    sys.exit()

""" def lex()
: go to next token in list, lines
if at the end of list terminate program
"""
def lex() :
    global token
    global cursor
    cursor += 1

    if cursor == len(lines) :
        sys.exit()
    token = lines[cursor]

""" def main()
: recieves a file as a system argument and splits the text
into a list of tokens
"""
import sys

with open(sys.argv[1]) as f :
    for w in f.read().lower().split():
        lines.append(w)
lines.append('EOF')
token = lines[0]
prog()

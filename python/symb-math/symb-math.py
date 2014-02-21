from pyparsing import Word, alphas, ParseException, Literal, CaselessLiteral \
, Combine, Optional, nums, Or, Forward, ZeroOrMore, StringEnd, alphanums

class Number:
	def __init__(self, value):
		self.value = value


class Value:
	def __init__(self, name):
		self.name = name


class BinOp:
    def __init__(self, left, right, op):
	    self.left = left
#		self.right = right
#		self.op = op


def pushFirst( str_, loc, toks ):
    print "===================================="
    print "str = " + str(str_)
    print "loc = " + str(loc)
    print "toks = " + str(toks)

	
point = Literal('.')
integer = Word(nums)
floatnumber = Combine( integer +
                       Optional( point + Optional(integer) )
                     )
ident = Word(alphas,alphanums + '_')

plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )

lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()

addop  = plus | minus
multop = mult | div
unops  = minus

expop = Literal( "^" )
assign = Literal( "=" )

expr = Forward()

atom = ( ( floatnumber | integer | ident ).setParseAction(pushFirst) | 
         ( lpar + expr.suppress() + rpar )
       )

unexpr = ((unops + atom).setParseAction(pushFirst) | atom)
	   
factor = Forward()
factor << unexpr + ZeroOrMore( ( expop + factor ).setParseAction( pushFirst ) )
        
term = factor + ZeroOrMore( ( multop + factor ).setParseAction( pushFirst ) )

expr << term + ZeroOrMore( ( addop + term ).setParseAction( pushFirst ) )

bnf = Optional((ident + assign).setParseAction(pushFirst)) + expr

pattern =  bnf + StringEnd()

pattern.parseString( "-123+456*789" )
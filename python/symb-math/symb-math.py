from pyparsing import *
import pprint


class Element:
    def simplify(self):
        pass

    def can_be_simplified(self):
        pass


class Value(Element):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "( " + str(self.value) + " )"

    def __str__(self):
        return self.__repr__()


class Variable(Element):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "( " + str(self.name) + " )"

    def __str__(self):
        return self.__repr__()


class BinOp(Element):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def __repr__(self):
        return "( " + str(self.left) + " " \
               + str(self.op) + " "\
               + str(self.right) + " )"

    def __str__(self):
        return self.__repr__()


class ExOp(BinOp):
    def __init__(self, left, op, right):
        BinOp.__init__(left, op, right)


class MulDivOp(BinOp):
    def __init__(self, left, op, right):
        BinOp.__init__(left, op, right)


class AddSubOp(BinOp):
    def __init__(self, left, op, right):
        BinOp.__init__(left, op, right)


class UnOp(Element):
    def __init__(self, op, operand):
        self.operand = operand
        self.op = op

    def __repr__(self):
        return "( " + str(self.op) + " " \
               + str(self.operand) + " )"

    def __str__(self):
        return self.__repr__()


def addValue(str_, loc, toks):
    print "Value ===================================="
    print "str = " + str(str_)
    print "loc = " + str(loc)
    print "toks = " + str(toks)
    return Value(toks[0])


def addVariable(str_, loc, toks):
    print "Variable ===================================="
    print "str = " + str(str_)
    print "loc = " + str(loc)
    print "toks = " + str(toks)
    return Variable(toks)


def addBinOp(str_, loc, toks):
    print "BinOp ===================================="
    print "str = " + str(str_)
    print "loc = " + str(loc)
    print "toks = " + str(toks)
    return BinOp(toks[0], toks[1], toks[2])


def addUnOp(str_, loc, toks):
    print "UnOp ===================================="
    print "str = " + str(str_)
    print "loc = " + str(loc)
    print "toks = " + str(toks)
    return UnOp(toks[0], toks[1])


point = Literal('.')
integer = Word(nums)
floatnumber = Combine(integer +
                      Optional(point + Optional(integer)))
ident = Word(alphas, alphanums + '_')

plus = Literal("+")
minus = Literal("-")
mult = Literal("*")
div = Literal("/")

lpar = Literal("(").suppress()
rpar = Literal(")").suppress()

addop = plus | minus
multop = mult | div
unops = minus

expop = Literal("^")

expr = Forward()

atom = ((floatnumber | integer).setParseAction(addValue) |
        (ident).setParseAction(addVariable) |
        ( lpar + expr.suppress() + rpar )
)

unexpr = ((unops + atom).setParseAction(addUnOp) | atom)

factor = Forward()
factor << (unexpr | (unexpr + OneOrMore((expop + factor)).setParseAction(addBinOp)))

term = (((factor + OneOrMore((multop + factor))).setParseAction(addBinOp)) | factor)

expr << (((term + OneOrMore((addop + term)))
          .setParseAction(lambda s, l, t: AddSubOp(t[0], t[1], t[2])))
         | term)

results = expr.parseString("-123+456*789")
pprint.pprint(results.asList())

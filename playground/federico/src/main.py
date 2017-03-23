
import sys
from antlr4 import *
from cGrammarLexer import cGrammarLexer
from cGrammarParser import cGrammarParser
# from cGrammarPrinter import cGrammarPrinter

def main(argv):
    input = FileStream(argv[1])
    lexer = cGrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = cGrammarParser(stream)
    tree = parser.program()

    # printer = cGrammarPrinter()
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)
    # print()

if __name__ == '__main__':
    main(sys.argv)
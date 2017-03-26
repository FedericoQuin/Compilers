
import sys
from antlr4 import *
from cGrammarLexer import cGrammarLexer
from cGrammarParser import cGrammarParser
from ASTCreator import ASTCreator

def main(argv):
    input = FileStream(argv[1])
    lexer = cGrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = cGrammarParser(stream)
    tree = parser.program()

    ASTbuilder = ASTCreator()
    walker = ParseTreeWalker()
    walker.walk(ASTbuilder, tree)
    print("\nAST:\n")
    print(ASTbuilder.printAST())
    print()
    print("\nFinished parsing file (and building AST) without any errors.")

if __name__ == '__main__':
    main(sys.argv)

import sys
from antlr4 import *
from cGrammarLexer import cGrammarLexer
from cGrammarParser import cGrammarParser
from ASTCreator import ASTCreator
from PTranslator import PTranslator

def main(argv):
    input = FileStream(argv[1])
    lexer = cGrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = cGrammarParser(stream)
    tree = parser.program()

    ASTbuilder = ASTCreator()
    walker = ParseTreeWalker()
    walker.walk(ASTbuilder, tree)


    ASTbuilder.toDot("data/output.dot")
    print("Abstract Syntax Tree saved to data/output.dot.")

    ast = ASTbuilder.getAST()
    translator = PTranslator()
    translator.translate(ast)
    translator.saveProgram("data/program.p")
    print("Created program text according to the Abstract Syntax Tree. (currently non functional)")


    print("\nFinished parsing file (and building AST) without any errors.\n")

if __name__ == '__main__':
    main(sys.argv)
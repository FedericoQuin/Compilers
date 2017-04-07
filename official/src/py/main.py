# To import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

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

    try:
        walker = ParseTreeWalker()
        walker.walk(ASTbuilder, tree)

        ast = ASTbuilder.getAST()

        translator = PTranslator()
        translator.translate(ast)

        translator.saveProgram("data/program.p")
        ASTbuilder.toDot("data/output.dot")

        print("Created program text according to the Abstract Syntax Tree. (currently non functional)")
        print("\nFinished parsing file (and building AST) without any errors.\n")

    except Exception as inst:
        ASTbuilder.toDot("data/output.dot")
        print(inst)
        print("\nERRORS!.\n")


    print("Abstract Syntax Tree saved to data/output.dot.")

   

if __name__ == '__main__':
    main(sys.argv)
import sys
from antlr4 import *
from src.cGrammarLexer import cGrammarLexer
from src.cGrammarParser import cGrammarParser
from src.py.AST.ASTCreator import ASTCreator
from src.py.PTranslator import PTranslator
from src.py.MyErrorListener import MyErrorListener


def runCompiler(cFilename, pFilename):
    input = FileStream(cFilename)
    lexer = cGrammarLexer(input)
    stream = CommonTokenStream(lexer)
    parser = cGrammarParser(stream)
    parser._listeners = [MyErrorListener(cFilename)]
    tree = parser.program()

    ASTbuilder = ASTCreator(stream)

    walker = ParseTreeWalker()
    walker.walk(ASTbuilder, tree)

    ast = ASTbuilder.getAST()
    ASTbuilder.toDot("data/output.dot")

    translator = PTranslator()
    translator.translate(ast, "data/symbolTable.txt", True)

    translator.saveProgram(pFilename)



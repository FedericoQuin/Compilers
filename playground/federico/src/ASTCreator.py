from cGrammarListener import cGrammarListener
from cGrammarParser import *
from AST.AST import AST

class ASTCreator(cGrammarListener):
    def __init__(self):
        self.AST = None

    def enterProgram(self, ctx:cGrammarParser.ProgramContext):
        self.AST = AST()

    def exitProgram(self, ctx:cGrammarParser.ProgramContext):
        pass


    def enterFunction(self, ctx:cGrammarParser.FunctionContext):
        pass

    def exitFunction(self, ctx:cGrammarParser.FunctionContext):
        pass


    def enterInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
        pass

    def exitInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
        pass


    def enterArguments(self, ctx:cGrammarParser.ArgumentsContext):
        pass

    def exitArguments(self, ctx:cGrammarParser.ArgumentsContext):
        pass


    def enterArgument(self, ctx:cGrammarParser.ArgumentContext):
        pass

    def exitArgument(self, ctx:cGrammarParser.ArgumentContext):
        pass


    def enterFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
        pass

    def exitFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
        pass


    def enterStatements(self, ctx:cGrammarParser.StatementsContext):
        pass

    def exitStatements(self, ctx:cGrammarParser.StatementsContext):
        pass


    def enterStatement(self, ctx:cGrammarParser.StatementContext):
        self.AST.addStatement(ctx)

    def exitStatement(self, ctx:cGrammarParser.StatementContext):
        pass

    def printAST(self):
        return str(self.AST)


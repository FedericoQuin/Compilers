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
        self.AST.enterBlock("FunctionBlock")

    def exitFunction(self, ctx:cGrammarParser.FunctionContext):
        self.AST.leaveBlock()


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
        # self.AST.addStatement(ctx)
        pass

    def exitStatement(self, ctx:cGrammarParser.StatementContext):
        pass


    def enterDeclaration(self, ctx:cGrammarParser.DeclarationContext):
        self.AST.addDeclaration(ctx)

    def exitDeclaration(self, ctx:cGrammarParser.DeclarationContext):
        pass

    
    def enterReturntype(self, ctx:cGrammarParser.ReturntypeContext):
        pass

    def exitReturntype(self, ctx:cGrammarParser.ReturntypeContext):
        pass

 # Enter a parse tree produced by cGrammarParser#initialization.
    def enterInitialization(self, ctx:cGrammarParser.InitializationContext):
        self.AST.addInitialization(ctx)

    # Exit a parse tree produced by cGrammarParser#initialization.
    def exitInitialization(self, ctx:cGrammarParser.InitializationContext):
        self.AST.endInitilization()


    # Enter a parse tree produced by cGrammarParser#lvalue.
    def enterLvalue(self, ctx:cGrammarParser.LvalueContext):
        pass

    # Exit a parse tree produced by cGrammarParser#lvalue.
    def exitLvalue(self, ctx:cGrammarParser.LvalueContext):
        pass


    # Enter a parse tree produced by cGrammarParser#rvalue.
    def enterRvalue(self, ctx:cGrammarParser.RvalueContext):
        self.AST.addRvalue(ctx)

    # Exit a parse tree produced by cGrammarParser#rvalue.
    def exitRvalue(self, ctx:cGrammarParser.RvalueContext):
        pass


    # Enter a parse tree produced by cGrammarParser#numericalvalue.
    def enterNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
        pass

    # Exit a parse tree produced by cGrammarParser#numericalvalue.
    def exitNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
        pass


    # Enter a parse tree produced by cGrammarParser#intvalue.
    def enterIntvalue(self, ctx:cGrammarParser.IntvalueContext):
        pass

    # Exit a parse tree produced by cGrammarParser#intvalue.
    def exitIntvalue(self, ctx:cGrammarParser.IntvalueContext):
        pass


    # Enter a parse tree produced by cGrammarParser#floatvalue.
    def enterFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
        pass

    # Exit a parse tree produced by cGrammarParser#floatvalue.
    def exitFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
        pass


    # Enter a parse tree produced by cGrammarParser#digits.
    def enterDigits(self, ctx:cGrammarParser.DigitsContext):
        pass

    # Exit a parse tree produced by cGrammarParser#digits.
    def exitDigits(self, ctx:cGrammarParser.DigitsContext):
        pass


    def printAST(self):
        return str(self.AST)

    def toDot(self, filename):
        dotFile = open(filename, 'w')
        dotFile.write(str(self.AST))
        dotFile.close()

    
    def getAST(self):
        return self.AST


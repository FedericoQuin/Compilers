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


    def enterAssignment(self, ctx:cGrammarParser.AssignmentContext):
        self.AST.addAssignment(ctx)

    def exitAssignment(self, ctx:cGrammarParser.AssignmentContext):
        self.AST.endAssignment()


    def enterLvalue(self, ctx:cGrammarParser.LvalueContext):
        pass

    def exitLvalue(self, ctx:cGrammarParser.LvalueContext):
        pass


    def enterRvalue(self, ctx:cGrammarParser.RvalueContext):
        self.AST.addRvalue(ctx)

    def exitRvalue(self, ctx:cGrammarParser.RvalueContext):
        pass


    def enterNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
        pass

    def exitNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
        pass


    def enterIntvalue(self, ctx:cGrammarParser.IntvalueContext):
        pass

    def exitIntvalue(self, ctx:cGrammarParser.IntvalueContext):
        pass


    def enterFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
        pass

    def exitFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
        pass


    def enterDigits(self, ctx:cGrammarParser.DigitsContext):
        pass

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


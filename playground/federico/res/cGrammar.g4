grammar cGrammar;


program : function;
function : returntype ID '(' initialargument ')' '{' function_body '}';

initialargument : 
	argument arguments
	|;
arguments :	
	',' argument arguments
	|;
argument : TYPE ID;

function_body : statements;

statements : 
	statement statements
	|;

statement : declaration;

declaration : TYPE ID ';';

returntype : TYPE | VOID;

VOID : 'void';
TYPE : 
	'char' '*'?
	|'float' '*'?
	|'int' '*'?;
ID : [a-zA-Z] ([a-zA-Z] | [0-9])*;

WS : [ \r\t\n]+ -> skip ;

SL_COMMENT : '//' .*? '\n' -> skip;
ML_COMMENT : '/*' (. | '\n')*? '*/' ->skip;

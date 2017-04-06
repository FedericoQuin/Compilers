
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
statement 
	: declaration ';'
	| assignment ';'
	;

declaration : TYPE ID;
assignment : lvalue '=' rvalue; // lack of better words

lvalue 
	: declaration 
	| ID;
rvalue 
	: CHARVALUE
	| numericalvalue; 		// NOTE: no differentiation between int value and pointer value, would match the same anyways


CHARVALUE : '\'' . '\'';
numericalvalue : floatvalue | intvalue;

intvalue : DIGIT DIGIT*;
floatvalue : digits? '.' digits;
DIGIT : [0-9];
NOTZERODIGIT : [1-9];
digits : DIGIT+;

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

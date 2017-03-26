grammar cGrammar;


program : function;
function : (TYPE | 'void') ID '(' initialargument ')' '{' function_body '}';

initialargument : 
	argument arguments
	|;
arguments :	
	',' argument arguments
	|;
argument : TYPE ID;

function_body : statements;
//function_body : (initialstatement | comments)*;

initialstatement : statement statements;
statements : 
	statement statements
	|;

statement : TYPE ID ';';

//comments : 
//	comment
//	| multilinecomment;

//comment : '//' (TEXT)*;
//multilinecomment: '/*' multilinecommenttext '*/';
//multilinecommenttext : TEXT; // TODO add exception for */


TYPE : 
	'char' '*'?
	|'float' '*'?
	|'int' '*'?;
ID : [a-zA-Z] ([a-zA-Z] | [0-9])*;
//TEXT : ([a-zA-Z] | [0-9])*;

WS : [ \r\t\n]+ -> skip ;

SL_COMMENT : '//' .*? '\n' -> skip;
ML_COMMENT : '/*' (. | '\n')*? '*/' ->skip;

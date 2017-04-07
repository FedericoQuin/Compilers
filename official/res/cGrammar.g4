
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
	: expression ';'
	| declaration ';'
	| ifelse
	;

expression :	// TODO add brackets
	lvalue OPERATOR_AS add_sub
	| add_sub
	| ID POST_OPERATOR_INCR
	| PRE_OPERATOR_INCR identifier		// NOTE: the prefix operators don't work for some mysterious reason
	| ID POST_OPERATOR_DECR
	| PRE_OPERATOR_DECR ID;

add_sub :
	add_sub OPERATOR_PLUS add_sub
	| add_sub OPERATOR_MINUS add_sub
	| identifier
	| rvalue
	| mul_div;

mul_div :
	mul_div OPERATOR_MUL mul_div
	| mul_div OPERATOR_DIV mul_div
	| identifier
	| rvalue;

OPERATOR_AS : '=';
OPERATOR_PLUS : '+';
POST_OPERATOR_INCR : '++';
POST_OPERATOR_DECR : '--';
PRE_OPERATOR_INCR : '++';
PRE_OPERATOR_DECR : '--';
OPERATOR_MINUS : '-';
OPERATOR_DIV : '/';
OPERATOR_MUL : '*';

OPERATOR_EQ : '==';
OPERATOR_NE : '!=';
OPERATOR_GT : '>';
OPERATOR_GE : '>=' | '=>';
OPERATOR_LT : '<';
OPERATOR_LE : '<=' | '=<';

OPERATOR_OR :
	'||'
	| 'or';
OPERATOR_AND :
	'&&'
	| 'and';
OPERATOR_NOT :
	'!'
	| 'not';

identifier : ID;

ifelse : 
	'if' '(' firstcondition ')' '{' first_true_statements '}'
	| 'if' '(' firstcondition ')' first_true_statement else_statement
	| 'if' '(' firstcondition ')' '{' first_true_statements '}' else_statement
	| 'if' '(' firstcondition ')' '{' first_true_statements '}' else_statement
	| 'if' '(' firstcondition ')' first_true_statement else_statement;

else_statement :
	 
	| 'else' first_false_statement
	| 'else' '{' first_false_statements '}';

// Hacks to build the AST
firstcondition : condition;
first_true_statements : statements;
first_true_statement : statement;
first_false_statement : statement;
first_false_statements : statements;

condition :
	condition OPERATOR_OR condition
	| LBRACKET condition RBRACKET	// Not supported yet
	| condition_and
	| comparison;

condition_and :
	condition_and OPERATOR_AND condition_and
	| condition_not
	| comparison;

condition_not :
	OPERATOR_NOT comparison;

comparison : 
	rvalue comparator rvalue
	| rvalue comparator ID
	| ID comparator rvalue
	| ID comparator ID;

comparator :
	OPERATOR_EQ
	| OPERATOR_NE
	| OPERATOR_GT
	| OPERATOR_GE
	| OPERATOR_LT
	| OPERATOR_LE;

LBRACKET : '(';
RBRACKET : ')';

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

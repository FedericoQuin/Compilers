
grammar cGrammar;


program :
	program functiondecl
	| program function
	|
	;

function : returntype ID '(' initialargument ')' '{' function_body '}';

functiondecl : returntype ID '(' initialargument ')' ';';

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
	| while_loop
	| for_loop
	| break_stmt ';'
	| continue_stmt ';'
	| return_stmt ';'
	;

break_stmt : 'break';
continue_stmt : 'continue';
return_stmt : 'return';

expression :	// TODO add brackets
	lvalue OPERATOR_AS add_sub
	| add_sub
	| ID POST_OPERATOR_INCR
	| PRE_OPERATOR_INCR lvalue_identifier		// NOTE: the prefix operators don't work for some mysterious reason
	| ID POST_OPERATOR_DECR
	| PRE_OPERATOR_DECR ID
	| condition;

add_sub :
	add_sub OPERATOR_PLUS add_sub
	| add_sub OPERATOR_MINUS add_sub
	| rvalue_identifier
	| rvalue
	| mul_div;

mul_div :
	mul_div OPERATOR_MUL mul_div
	| mul_div OPERATOR_DIV mul_div
	| rvalue_identifier
	| rvalue
	| bracket_expression;

bracket_expression :
	LBRACKET expression RBRACKET;

OPERATOR_AS : '=';
OPERATOR_PLUS : '+';
POST_OPERATOR_INCR : '++';
POST_OPERATOR_DECR : '--';
PRE_OPERATOR_INCR : '++';
PRE_OPERATOR_DECR : '--';
OPERATOR_MINUS : '-';
OPERATOR_DIV : '/';
OPERATOR_MUL : '*';

//////////////////////////////////////////////////////////
// If-else stuff and boolean conditions					//
//////////////////////////////////////////////////////////

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

lvalue_identifier : ID;
rvalue_identifier : ID;

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
	| condition_and
	| comparison;

condition_and :
	condition_and OPERATOR_AND condition_and
	| condition_not
	| comparison;

condition_not :
	OPERATOR_NOT comparison
	| bracket_condition;

bracket_condition :
	LBRACKET condition RBRACKET
	| OPERATOR_NOT LBRACKET condition RBRACKET;

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

//////////////////////////////////////////////////////////
// While loop stuff 									//
//////////////////////////////////////////////////////////

while_loop : 
	'while' '(' first_while_condition ')' '{' first_while_statements '}'
	| 'while' '(' first_while_condition ')' first_while_statement;

// Hacks to build the AST
first_while_statements : statements;
first_while_statement : statement;
first_while_condition : condition;


//////////////////////////////////////////////////////////
// For loop stuff 										//
//////////////////////////////////////////////////////////

for_loop : 
	'for' '(' first_stmt_for ';' second_stmt_for ';' third_stmt_for ')' '{' first_for_statements '}'
	| 'for' '(' first_stmt_for ';' second_stmt_for ';' third_stmt_for ')' first_for_statement;

// Hacks to build the AST
first_for_statements : statements;
first_for_statement : statement;
first_stmt_for :
	expression
	| declaration
	| ;

second_stmt_for :
	expression
	| declaration
	| ;

third_stmt_for :
	expression
	| declaration
	| ;





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
ID : ([a-zA-Z] | '_') ([a-zA-Z] | [0-9] | '_')*;




WS : [ \r\t\n]+ -> skip ;

SL_COMMENT : '//' .*? '\n' -> skip;
ML_COMMENT : '/*' (. | '\n')*? '*/' ->skip;

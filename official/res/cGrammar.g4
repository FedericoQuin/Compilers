
grammar cGrammar;


program :
	program functiondecl
	| program function
	| program global_declaration ';'
	| program include_file  
	|
	;


include_file : 
	INCLUDE_FILE;


function : returntype ID '(' initialfunctionargument ')' '{' function_body '}';

functiondecl : returntype ID '(' initialfunctionargument ')' ';';

initialfunctionargument : 
	type_argument type_arguments
	|;
type_arguments :	
	',' type_argument type_arguments
	|;
type_argument : dec_type ID;



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
	| scanf ';'
	| printf ';'
	;

break_stmt : 'break';
continue_stmt : 'continue';
return_stmt : RETURN expression?;

expression :	// TODO add brackets
	lvalue OPERATOR_AS add_sub
	| add_sub
	| ID POST_OPERATOR_INCR
	| PRE_OPERATOR_INCR lvalue_identifier		// NOTE: the prefix operators don't work for some mysterious reason
	| ID POST_OPERATOR_DECR
	| PRE_OPERATOR_DECR ID
	| condition
	| rvalue;

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


//////////////////////////////////////////////////////////
// If-else stuff and boolean conditions					//
//////////////////////////////////////////////////////////


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
	| rvalue comparator rvalue_identifier
	| rvalue_identifier comparator rvalue
	| rvalue_identifier comparator rvalue_identifier;

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

//////////////////////////////////////////////////////////
// Scanf and Printf										//
//////////////////////////////////////////////////////////

scanf : 'scanf' '(' format_string call_arguments ')';
printf : 'printf' '(' format_string call_arguments ')';

// Not sure how to go about this in a decent manner
format_string : STRING;


//////////////////////////////////////////////////////////
// Function calls 										//
//////////////////////////////////////////////////////////
functioncall :
	ID '(' call_argument_initial ')';

call_argument_initial :
	rvalue call_arguments
	| rvalue_identifier call_arguments
	|;

call_arguments :
	',' call_argument call_arguments
	|;

// TODO verify this
call_argument :
	rvalue
	| rvalue_identifier;



//////////////////////////////////////////////////////////
// Declarations and assignments							//
//////////////////////////////////////////////////////////

declaration : 
	normal_declaration
	| array_declaration;

normal_declaration :
	dec_type ID initialization
	| dec_type ID;
array_declaration : 
	dec_type ID LSQUAREBRACKET digits RSQUAREBRACKET;

assignment : lvalue OPERATOR_AS expression; // lack of better words

initialization :
	OPERATOR_AS expression;

global_declaration : 
	declaration;




//////////////////////////////////////////////////////////
// LValues and RValues									//
//////////////////////////////////////////////////////////

lvalue 
	: ID
	| arrayelement_lvalue;

rvalue 
	: charvalue
	| numericalvalue 		// NOTE: no differentiation between int value and pointer value, would match the same anyways
	| functioncall
	| arrayelement_rvalue;

arrayelement_rvalue : arrayelement;
arrayelement_lvalue : arrayelement;

arrayelement :
	ID LSQUAREBRACKET digits RSQUAREBRACKET
	| ID LSQUAREBRACKET ID RSQUAREBRACKET;



charvalue : CHARVALUE;
numericalvalue : floatvalue | intvalue;

intvalue : OPERATOR_MINUS? DIGIT DIGIT*;
floatvalue : OPERATOR_MINUS? digits? '.' digits;





digits : DIGIT+;
returntype : dec_type | VOID;

dec_type : 
	CHAR ptr
	| FLOAT ptr
	| INT ptr;


ptr : 
	'*' ptr
	|;




INCLUDE_MACRO : '#include';
INCLUDE_FILE : 
	INCLUDE_MACRO OPERATOR_LT .*? OPERATOR_GT
	| INCLUDE_MACRO ' '* OPERATOR_LT .*? OPERATOR_GT;


LSQUAREBRACKET : '[';
RSQUAREBRACKET : ']';
LBRACKET : '(';
RBRACKET : ')';
CHARVALUE : '\'' . '\'';
RETURN : 'return';


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


VOID : 'void';
CHAR : 'char';
FLOAT : 'float';
INT : 'int';

DIGIT : [0-9];
NOTZERODIGIT : [1-9];
ID : ([a-zA-Z] | '_') ([a-zA-Z] | [0-9] | '_')*;
POINT : '.';
STRING : '"' .*? '"';

WS : [ \r\t\n]+ -> skip ;

SL_COMMENT : '//' .*? '\n' -> skip;
ML_COMMENT : '/*' (. | '\n')*? '*/' ->skip;

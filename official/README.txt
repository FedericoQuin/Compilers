Federico Quin s0142520
Sam Mylle s0142520
University Of Antwerp
2017

Main structure:
	To build the project, use the following command: make build.
	This will provide a file named c2p.py.

	To compile a c-file, use the following command: python3 c2p.py <cfile>
	Where <cfile> is the relative path to the c-file you wish to compile.
	The output of a (correct) c-file will appear in the ./data folder.

Output:
	Currently, there are 3 output files which are generated: output.dot, program.p and symbolTable.txt.
	output.dot contains the decorated AST of the compiled c program.
	program.p is currently empty, in the future it will contain the translation of the c code to p code.
	symbolTable.txt contains the symbol table of the c program. More info can be founf in the file itself.

Test structure:
	To run the tests, you must use the following command: make test.
	The tests that are currently being can be found in src/tests.
	The files these tests manipulate are found in res/test and res/solutions.
	Which functionality is being tested should be clear by the name of the c files in res/test.

Extra features:
	Currently, we have added the following extra features:
		- for loops
		- break and continue statement
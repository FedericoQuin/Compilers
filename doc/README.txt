Federico Quin s0140938
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
	symbolTable.txt contains the symbol table of the c program. More info can be founf in the file itself.

Test structure:
	To run the tests, you must use the following command: make test.
	The tests that are currently being run can be found in src/tests.
	The files these tests use as validation are found in res/solutions.
	The input file that corresponds to this solution can be found in res/happyDayTests.
	Which functionality is being tested should be clear by the name of the provided c files.
	There are also death tests input files which can be found in res/deathTests. They require no solution files compared to the files in res/happyDayTests.

Extra features:
	We have added the following extra features:
		- for loops
		- break and continue statement
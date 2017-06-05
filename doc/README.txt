Federico Quin s0140938
Sam Mylle s0142520
University Of Antwerp
2017

Main structure:
	To build the project, use the following command: make build.
	This will provide a file named c2p.py.

	To compile a c-file, use the following command: python3 c2p.py <cfile> <pfile>
	Where <cfile> is the relative path to the c-file you wish to compile.
		  <pfile> is the relative path to where you want the translated program (uses 'data/program.p' by default if not provided).
	The output (AST in dot format, p program if not provided as argument) of a (correct) c-file will appear in the ./data folder.

Output:
	Currently, there are 2 output files which are generated: 'output.dot' and 'program.p'.
	
	> output.dot contains the decorated AST of the compiled c program.
	> program.p contains the translation of the c program (to p code).

Test structure:
	NOTE: in order to run the tests, 'pytest' needs to be installed.

	To run the tests, you must use the following command: make test.
	The tests that are currently being run can be found in 'src/tests/run_tests.py'.
	The files these tests use as validation are found in 'res/solutions'.
	The input file that corresponds to the solution can be found in 'res/happyDayTests'.
	Which functionality is being tested should be clear by the name of the provided c files.

	Running all the tests will run succesful tests, as well as death tests. 
	The death tests can be found in 'res/deathTests'. They require no solution files compared to the files in 'res/happyDayTests'.

Extra features:
	We have added the following extra features:
		- for loops
		- break and continue statement
		- boolean variables

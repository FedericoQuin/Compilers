import sys
from src.py.runCompiler import runCompiler

def translateProgram(argv):
	cFilename = ""
	pFilename = ""
	if len(argv) == 2:
		# For own convenience
		pFilename = "data/program.p"
	elif len(argv) != 3:
		print("Please run this program with 2 arguments: the c program filename and the p output filename.")
		return
	else:
		pFilename = argv[2]
	
	cFilename = argv[1]

	try:
		runCompiler(cFilename, pFilename)
	except Exception as inst:
		print(inst)
		
if __name__ == "__main__":
	translateProgram(sys.argv)

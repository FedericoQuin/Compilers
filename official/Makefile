
.PHONY : build install test

build:
	@java -jar antlr/antlr-4.6-complete.jar -Dlanguage=Python3 res/cGrammar.g4 -visitor
	@mv res/*.tokens src/
	@mv res/*.py src/

	@cp res/runScript/c2p.py ./
	@echo "Project built correctly."

install: build

test:
	@pytest ./src/tests/run_tests.py


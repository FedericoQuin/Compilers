
.PHONY : build install test grammar all

build: grammar
	@cp res/runScript/c2p.py ./
	@echo "Project built correctly."

install: build

all: build

test: grammar
	@pytest --tb=short ./src/tests/run_tests.py

grammar:
	@java -jar antlr/antlr-4.6-complete.jar -Dlanguage=Python3 res/cGrammar.g4 -visitor
	@mv res/*.tokens src/
	@mv res/*.py src/
	@echo "Compiled language without errors."

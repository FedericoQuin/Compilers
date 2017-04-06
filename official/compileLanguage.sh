if [ "$#" -ne 1 ]; then
	echo "Enter the name of the grammar file (located in res directory)."
	echo "For example: grammar"
else
	java -jar antlr/antlr-4.6-complete.jar -Dlanguage=Python3 res/"$1".g4 -visitor
	if [ "$?" -eq 0 ]; then
		mv res/"$1".tokens src/"$1".tokens
		mv res/"$1"Lexer.py src/"$1"Lexer.py
		mv res/"$1"Lexer.tokens src/"$1"Lexer.tokens
		mv res/"$1"Listener.py src/"$1"Listener.py
		mv res/"$1"Parser.py src/"$1"Parser.py
		mv res/"$1"Visitor.py src/"$1"Visitor.py
		exit 0
	fi
fi

exit 1
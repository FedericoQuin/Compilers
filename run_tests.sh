cd official
sh compileLanguage.sh cGrammar
if [ "$?" -eq 0 ]; then
	cd ..
	pytest ./official/src/tests/run_tests.py
	exit "$?"
fi

exit 1


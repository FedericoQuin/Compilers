cd official
sh compileLanguage.sh cGrammar
if [ "$?" -eq 0 ]; then
	cd ..
	pytest ./official/src/tests/run_tests.py

	if [ "$?" -eq 0 ]; then
		echo "OK"
	else
		echo "NOK"
	fi

	exit "$?"
fi

exit 1


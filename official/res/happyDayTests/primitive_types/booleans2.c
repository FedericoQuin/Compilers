
bool testing(bool& test) {
	test = false;
	return !test;
}


int main() {
	int a = 5;

	bool cond = (a >= 5);

	bool result = testing(cond);

	if (cond == false) {
		return a;
	}

	return 3;
}

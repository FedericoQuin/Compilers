
bool test1() {
	return true;
}

bool test2() {
	return !test1();
}

int main() {
	if (test2() == false) {
		return 10;
	} else {
		return 15;
	}
}


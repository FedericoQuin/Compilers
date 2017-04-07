int main(int argc, char* argv) {
	int x = 0;
	int y = 0;

	// Both braces
	if (! x < 5 && y == 6) {
		int a;
	} else {
		int b;
	}

	// else no braces
	if (x <= 5 or y == 6) {
		int a;
		int moarDecl;
	} else
		int b;

	// if no braces
	if (x > 5 and y == 6)
		int a;
	else {
		int b;
	}

	// Both no braces
	if (x >= 5 || ! y == 6)
		int a;
	else
		int b;
	int testDecl = 5;

	// Cool structure
	if (x == 5 || ! y == 6)
		int a;
	else if (x >= 8) {
		int omaigodsocool = 10;
	}
}
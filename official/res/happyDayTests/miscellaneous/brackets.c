int main() {
	int a = (5 + 4) * 3;
	a = 3 * (5 + 4);

	int b = 5;
	int c = 3;
	while ( a > b && !(b > c || c < b) ) {
		b = b + 1;
	}

	b = 5;
	while ((b > c || c < b) && a > b) {
		b = b + 1;
	}
}
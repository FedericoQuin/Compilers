

int main() {
	int* a[10];

	a[5] = 2; // Conversion from int to address

	int b = 10;
	a[4] = &b;
	*(a[4]) = 20;

	printf("New value: %i.\n", b);
}


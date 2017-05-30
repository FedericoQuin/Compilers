
// Just for fun :D

#include <stdio.h>

int fac_rec(int i) {
	if (i == 0) {
		return 1;
	}
	return i * fac_rec(i-1);
}

int fac_iter(int amt) {
	int result = 1;

	for (int i = 1; i <= amt; i = i + 1) {
		result = result * i;
	}

	return result;
}

int main() {
	int value;
	printf("Enter factorial value: ");
	scanf("%i", value);
	printf("\n\n");

	printf("Factorial return value (recursive): %i.\n", fac_rec(value));
	printf("Factorial return value (iterative): %i.\n", fac_iter(value));
	return 0;
}


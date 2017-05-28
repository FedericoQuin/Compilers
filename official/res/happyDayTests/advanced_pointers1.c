
#include <stdio.h>

int main() {
	int* a[10];
	int b = 20;

	a[5] = &b;

	**(a + 5) = 25;

	printf("New value for b: %i.\n", b);
}


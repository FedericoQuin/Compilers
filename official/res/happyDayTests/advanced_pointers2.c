
#include <stdio.h>


void doSomething(int*& a) {
	*a = 100;
}

int main() {
	int* a;
	int b = 20;

	a = &b;

	doSomething(a);

	printf("New value should be 100: %i.\n", b);
}

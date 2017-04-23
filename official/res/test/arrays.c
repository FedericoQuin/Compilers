int main() {
	int a[10];
	for (int i = 0; i < 10; i++) {
		a[i] = i;
	}

	char* b[100];
	doSomething(b[20]);

	float pointerArray[5];
	if (pointerArray[0] > 0) {
		pointerArray[2] = 50.0;
	}
}
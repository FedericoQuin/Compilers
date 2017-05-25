

void doSomething(char* test) {
	return;
}

int main() {
	int a[10];
	for (int i = 0; i < 10; i = i + 1) {
		a[i] = i;
	}

	char* b[100];
	doSomething(b[20]);

	float pointerArray[5];
	if (pointerArray[0] > 0.0) {
		pointerArray[2] = 50.0;
	}
	int index = 10;

	b[index * 2 + 10] = 10;
}
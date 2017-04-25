// check for array elements

int someFunction(char a, float b) {
	if (a == 'a') {
		return 1;
	} else if (b == 4.9) {
		return 10;
	}
}

int main() {
	char charArray[100];
	float floatArray[50];
	int intArray[20];

	int result = someFunction(intArray[10], floatArray[36]);
}
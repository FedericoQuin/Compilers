

int main() {
	int*** a[10];

	int**** b = a;

	*(**(b) + 1) = 5;

	int* var1;
	int* var2;

	float array[20];
	*var1 = 5;
	*var2 = 10;

	float* arrayPtr = array;

	*(arrayPtr + *(var1) + *(var2)) = 2.00;

}

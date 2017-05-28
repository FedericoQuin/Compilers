

int main() {
	int*** a[10];

	int**** b = a;

	int var1 = 10;
	int var2 = 5;
	int* var1_p = &var1;
	int* var2_p = &var2;

	float array[20];
	*var1_p = 5;
	*var2_p = 10;

	float* arrayPtr = array;

	int temp = 5;
	*(arrayPtr + temp) = 2.73;
	*(arrayPtr + *(var1_p) + *(var2_p)) = 2.001;
	return *var2_p;
}



int main() {
	int a[20];
	int* b = a;

	*(b+1) = 20;

	int* p1 = b + 1;
	int**p2 = &p1;
	int*** p3 = &p2;

	// Who would even write code like this
	(*(*((*p3)))) = 6;

	int d = ***p3;

	return d;
}
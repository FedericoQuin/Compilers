

int main() {
	int a[20];
	int* b = a;

	*(b+1) = 20;

	int*** c = 0;
	// Who would even write code like this
	(*(*((*c)))) = 5;

	**(*c) = 39;

	int d = ***c;
}
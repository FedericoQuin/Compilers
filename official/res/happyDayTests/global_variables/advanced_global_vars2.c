
int a = 10;


int* getAddressA() {
	return &a;
}

void manipGlobalVariable(int valueTo) {
	*getAddressA() = valueTo;
}

int main() {
	manipGlobalVariable(23);
	
	return a;
}

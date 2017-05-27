
int SomeArrayToDoAnoying[5];
int GLOBALVAR1[5];
int GLOBALVAR2 = 5;
int GLOBALVAR3 = GLOBALVAR1[1] + GLOBALVAR2;

int modifyGlobal() {
	GLOBALVAR1[1] = 3;
	GLOBALVAR3 = GLOBALVAR3 + 50 + GLOBALVAR1[1];
	return 0;
}

int someVar = modifyGlobal();

int main() {
	return GLOBALVAR3;
}



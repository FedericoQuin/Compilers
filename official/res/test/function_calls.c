
int getCookies();
int getCookies2(int idk);
int getCookies3(char woeps, float no, int ja);
int getOtherCookies(int test, char test2, float test3);


int main() {
	int a = 5;
	getCookies();
	getCookies2(a);
	getCookies3('a', 2.9, 8);

	char var2 = 'a';
	int b = 5 + getOtherCookies(a, var2, 0.9);
}
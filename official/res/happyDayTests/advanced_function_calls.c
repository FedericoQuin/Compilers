
int getCookies(int& a) {a = 10; return a;}
int getCookies2(int idk) {return idk;}
int getCookies3(char woeps, float no, int ja) {
	if (no == 5.0) {
		return ja;
	} else {
		return ja+1;
	}
}
int getOtherCookies(int test, char test2, float test3) {return 9001 + test;}


int main() {
	int a = 5;
	getCookies(a);
	getCookies2(a);
	getCookies3('a', 2.9 + 5.3, (a + 3) * 5);

	char var2 = 'a';
	int b = 5 + getOtherCookies(a * 2, (var2), (0.9) / 5.0 + 3.0);

	return b;
}
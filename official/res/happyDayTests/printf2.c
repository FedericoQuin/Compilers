
#include <stdio.h>

void printMyFloat(float& myFloat) {
	printf("This is my special float: %f.\n", myFloat);
}

int main() {
	char word[5];

	word[0] = 'H';
	word[1] = 'e';
	word[2] = 'l';
	word[3] = 'l';
	word[4] = 'o';

	printf("This is my word: %s\n", word);

	float yes = 5.3684;
	printMyFloat(yes);
}

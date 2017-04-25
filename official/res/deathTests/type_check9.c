int something() {return 0;}

float thatOtherFunction(int a, float c) {return c;}

int main() {
	float wow = thatOtherFunction(something(), something());
}

bool* just__why____(bool* just_bcuz_idk) {
	*just_bcuz_idk = true;
	return just_bcuz_idk;
}

int main() {
	bool yes = false;

	bool* no = &yes;

	no = just__why____(no);

	if (*no == true) {
		return 3;
	}
	return 1;
}


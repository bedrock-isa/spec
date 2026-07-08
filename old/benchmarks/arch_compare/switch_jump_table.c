switch_jump_table(int x, int bias) {
	switch (x & 7) {
	case 0: return bias + 3;
	case 1: return bias + 5;
	case 2: return bias + 7;
	case 3: return bias + 11;
	case 4: return bias + 13;
	case 5: return bias + 17;
	case 6: return bias + 19;
	default: return bias + 23;
	}
}

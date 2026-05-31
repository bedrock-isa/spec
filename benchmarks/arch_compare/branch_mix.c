branch_mix(int *p, int n) {
	int i;
	int acc;
	int v;

	i = 0;
	acc = 0;
	while (i < n) {
		v = p[i];
		if (v > 0) {
			acc = acc + v;
		} else {
			acc = acc - v;
		}
		i = i + 1;
	}
	return acc;
}

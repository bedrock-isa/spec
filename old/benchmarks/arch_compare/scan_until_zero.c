scan_until_zero(int *p, int n) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = p[i];
		if (v == 0) {
			return i;
		}
		i = i + 1;
	}
	return i;
}

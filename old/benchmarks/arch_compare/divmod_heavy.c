divmod_heavy(int *p, int n, int d) {
	int i;
	int acc;
	int v;
	int q;
	int r;

	i = 0;
	acc = 0;
	while (i < n) {
		v = p[i] + i;
		q = v / d;
		r = v % d;
		acc = acc + q * 3 + r * 5;
		i = i + 1;
	}
	return acc;
}

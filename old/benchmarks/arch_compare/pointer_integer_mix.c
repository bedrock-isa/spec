pointer_integer_mix(int *base, int *limit, int n, long byte_bias) {
	int *p;
	int *q;
	long span;
	int acc;
	int i;

	p = base + n;
	q = base + byte_bias / 4;
	span = limit - base;
	i = 0;
	acc = 0;
	while (i < n) {
		acc = acc + *p + *q;
		p = p + 1;
		q = q + 1;
		if (span < i) {
			acc = acc + 1;
		}
		i = i + 1;
	}
	return acc;
}

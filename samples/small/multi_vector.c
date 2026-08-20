mv_sum(int *p, int n) {
	int i;
	int acc;

	i = 0;
	acc = 0;
	while (i < n) {
		acc = acc + p[i];
		i = i + 1;
	}
	return acc;
}

mv_dot(int *a, int *b, int n) {
	int i;
	int acc;
	int av;
	int bv;

	i = 0;
	acc = 0;
	while (i < n) {
		av = a[i];
		bv = b[i];
		acc = acc + av * bv;
		i = i + 1;
	}
	return acc;
}

mv_clamp_store(int *dst, int *src, int n, int lo, int hi) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = src[i];
		if (v < lo) {
			v = lo;
		}
		if (v > hi) {
			v = hi;
		}
		dst[i] = v;
		i = i + 1;
	}
	return i;
}

mv_pipeline(int *dst, int *a, int *b, int n, int lo, int hi) {
	int s;
	int d;

	mv_clamp_store(dst, a, n, lo, hi);
	s = mv_sum(dst, n);
	d = mv_dot(a, b, n);
	return s + d;
}

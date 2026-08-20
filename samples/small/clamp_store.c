clamp_store(int *dst, int *src, int n, int lo, int hi) {
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

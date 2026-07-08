scale_store(int *dst, int *src, int n) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = src[i];
		dst[i] = v * 4 + 1;
		i = i + 1;
	}
	return i;
}

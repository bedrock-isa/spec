ms_find_zero(int *p, int n) {
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

ms_count_ge(int *p, int n, int threshold) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = p[i];
		i = i + 1;
		if (v >= threshold) {
			break;
		}
	}
	return i;
}

ms_copy_prefix(int *dst, int *src, int n) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = src[i];
		dst[i] = v;
		if (v == 0) {
			return i;
		}
		i = i + 1;
	}
	return i;
}

ms_pipeline(int *dst, int *src, int n, int threshold) {
	int z;
	int c;
	int copied;

	z = ms_find_zero(src, n);
	c = ms_count_ge(src, n, threshold);
	copied = ms_copy_prefix(dst, src, n);
	return z + c + copied;
}

block_copy_long(long *dst, long *src, int n) {
	int i;

	i = 0;
	while (i < n) {
		dst[i] = src[i];
		i = i + 1;
	}
	return i;
}

copy_words(int *dst, int *src, int n) {
	int i;

	i = 0;
	while (i < n) {
		dst[i] = src[i];
		i = i + 1;
	}
	return i;
}

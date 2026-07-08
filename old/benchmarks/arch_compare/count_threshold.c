count_threshold(int *p, int n, int threshold) {
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

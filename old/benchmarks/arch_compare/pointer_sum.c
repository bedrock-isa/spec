sum(int *p, int n) {
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

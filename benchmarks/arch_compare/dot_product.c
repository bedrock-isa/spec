dot_product(int *a, int *b, int n) {
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

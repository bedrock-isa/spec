int ext_add();
int ext_mix();
int ext_fold();

call_heavy(int *p, int n) {
	int i;
	int acc;
	int v;

	i = 0;
	acc = 0;
	while (i < n) {
		v = p[i];
		acc = ext_add(acc, v);
		acc = ext_mix(acc, i);
		acc = ext_fold(acc, v + i);
		i = i + 1;
	}
	return acc;
}

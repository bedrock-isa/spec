spill_heavy_loop(int *a, int *b, int *c, int *d, int n) {
	int i;
	int s;
	int t;
	int u;
	int v;
	int w;
	int x;
	int y;
	int z;

	i = 0;
	s = 1;
	t = 2;
	u = 3;
	v = 4;
	w = 5;
	x = 6;
	y = 7;
	z = 8;
	while (i < n) {
		s = s + *a;
		t = t + *b + s;
		u = u + *c + t;
		v = v + *d + u;
		w = w + s + v;
		x = x + t + w;
		y = y + u + x;
		z = z + v + y;
		a = a + 1;
		b = b + 1;
		c = c + 1;
		d = d + 1;
		i = i + 1;
	}
	return s + t + u + v + w + x + y + z;
}

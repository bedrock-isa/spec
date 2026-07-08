register_pressure(int *p, int n) {
	int i;
	int a;
	int b;
	int c;
	int d;
	int e;
	int f;
	int g;
	int h;
	int t;

	i = 0;
	a = 1;
	b = 2;
	c = 3;
	d = 4;
	e = 5;
	f = 6;
	g = 7;
	h = 8;
	while (i < n) {
		t = *p;
		p = p + 1;
		a = a + t;
		b = b + a;
		c = c + b;
		d = d + c;
		e = e + d;
		f = f + e;
		g = g + f;
		h = h + g;
		i = i + 1;
	}
	return a + b + c + d + e + f + g + h;
}

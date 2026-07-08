mixed_field_offsets(int *ip, long *lp, int n) {
	int a;
	int b;
	long x;
	long y;

	a = ip[1];
	b = ip[7];
	x = lp[2];
	y = lp[5];
	lp[5] = x + y + a + n;
	ip[7] = a + b + n;
	return ip[0] + ip[7];
}

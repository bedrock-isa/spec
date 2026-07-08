fir_three(int *dst, int *src, int n, int ca, int cb, int cc) {
	int i;
	int va;
	int vb;
	int vc;
	int out;

	i = 0;
	while (i < n) {
		va = src[i];
		vb = src[i + 1];
		vc = src[i + 2];
		out = va * ca;
		out = out + vb * cb;
		out = out + vc * cc;
		dst[i] = out;
		i = i + 1;
	}
	return i;
}

mf_fir_three(int *dst, int *src, int n, int ca, int cb, int cc) {
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

mf_scale_store(int *dst, int *src, int n) {
	int i;
	int v;

	i = 0;
	while (i < n) {
		v = src[i];
		dst[i] = v * 4 + 1;
		i = i + 1;
	}
	return i;
}

mf_bias_sum(int *p, int n, int bias) {
	int i;
	int acc;

	i = 0;
	acc = 0;
	while (i < n) {
		acc = acc + p[i] + bias;
		i = i + 1;
	}
	return acc;
}

mf_pipeline(int *tmp, int *dst, int *src, int n, int ca, int cb, int cc) {
	int a;
	int b;

	a = mf_fir_three(tmp, src, n, ca, cb, cc);
	b = mf_scale_store(dst, tmp, n);
	return mf_bias_sum(dst, n, a + b);
}

bitfield_ops(int x, int y) {
	int field;
	int cleared;
	int insert;

	field = (x >> 5) & 31;
	cleared = y & -993;
	insert = field << 5;
	return cleared | insert | (x & 7);
}

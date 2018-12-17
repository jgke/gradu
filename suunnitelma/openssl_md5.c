a += k + t + F(b, c, d);
a = ROTATE(a,s);
a += b;

a += k + t + (((c ^ d) & b) ^ d);
a = ((a << s) | ((a & 0xffffffff) >> (32 - s)));
a += b;

a += k + t + (((c ^ d) & b) ^ d);
a = a <<< s;
a += b;

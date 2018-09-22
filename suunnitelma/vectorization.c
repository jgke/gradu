#include <stddef.h>
#include "fns.h"

int fn_iter(int *restrict arr_a, int *restrict arr_b) {
    int res = 0;
    while(*arr_a)
        res += *(arr_a++) + *(arr_b++);
    return res;
}

int fn_size(int *restrict arr_a, int *restrict arr_b, size_t size) {
    int cur;
    int res = 0;
    for(cur = 0; cur < size; cur++)
        res += arr_a[cur] + arr_b[cur];
    return res;
}

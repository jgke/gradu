int strcmp(const char *a, const char *b) {
    while(*a && *b) {
        if(*a == *b) {
            a++;
            b++;
        }
        else {
            return *a - *b;
        }
    }
    return 0;
}

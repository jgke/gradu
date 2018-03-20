#include <stdio.h>
#include <limits.h>

void print_if_overflow(int x) {
    if(x + 1 <= x)
        printf("Overflow\n");
    else
        printf("Variable did not overflow\n");
}

int main(int argc, char *argv[]) {
    print_if_overflow(INT_MAX);
}

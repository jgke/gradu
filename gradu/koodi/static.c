int foo() {
    static int i = 0;
    return i++;
}

void main() {
    printf("%d\n", foo());
    printf("%d\n", foo());
}

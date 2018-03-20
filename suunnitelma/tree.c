#include <stdio.h>

typedef struct Tree {
    int value;
    struct Tree *left;
    struct Tree *right;
} Tree;

void printTree(int n, Tree *tree) {
    if(!tree) {
        printf("%*cLeaf\n", n, ' ');
    }
    else {
        printf("%*c[Branch %d\n", n, ' ', tree->value);
        printTree(n+2, tree->left);
        printTree(n+2, tree->right);
        printf("%*c]\n", n, ' ');
    }
}

int main() {
    Tree *a = NULL;
    Tree b = { 5, NULL, NULL };
    Tree c_left = { 3, NULL, NULL };
    Tree c = { 7, &c_left, NULL};
    Tree d = { 2, &b, &c };
    Tree e = { 1, a, &d };
    printTree(0, &e);
}

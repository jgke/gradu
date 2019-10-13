// Laajentamaton versio

#define LISAA_JA_TULOSTA(a, b) \
    do {\
        int tmp = a + b; \
        printf("Tulos: %d", tmp); \
    }

int tmp = 1;
LISAA_JA_TULOSTA(tmp, 1);

// laajennettu versio

int tmp = 1;
do { int tmp = tmp + 1; printf("Tulos: %d", tmp); };

#define LISAA_JA_TULOSTA(a, b) \
    do {\
        int tmp = a + b; \
        printf("Tulos: %d", tmp); \
    } while(0)

int tmp = 1;
LISAA_JA_TULOSTA(tmp, 1);

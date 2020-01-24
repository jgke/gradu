#include <stdint.h>

struct SuccessOrFailure {
    union {
        int32_t success;
        char *failure;
    } value;
    enum {
        _SUCCESS,
        _FAILURE
    } type;
};

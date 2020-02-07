struct Puu;

enum _Puu_d {
    _PUU_LEHTI,
    _PUU_HAARA,
};

struct _Puu_Lehti {
    int _1;
};

struct _Puu_Haara {
    struct Puu *_1;
    struct Puu *_2;
};

struct Puu {
    enum _Puu_d v;
    union {
        struct _Puu_Lehti Lehti;
        struct _Puu_Haara Haara;
    };
};

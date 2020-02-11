struct Puu;

struct _Puu_Lehti { struct Puu *_d; int _1; };

struct _Puu_Haara { struct Puu *_1; struct Puu *_2; };

union Puu { struct _Puu_Lehti Lehti; struct _Puu_Haara Haara; };

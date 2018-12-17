enum ColorEnum {
    Red, Green, Blue, Grayscale, RGB, RGBA
};

struct Color {
    enum ColorEnum type;
    union {
        struct {} empty; // Red, Green, Blue
        char grayscale; // Grayscale
        struct { char red, green, blue; } rgb; // RGB
        struct { char red, green, blue, alpha; } rgba; // RGBA
    } d;
};

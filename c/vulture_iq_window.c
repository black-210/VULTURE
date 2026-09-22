#include "vulture_iq_window.h"
#include <math.h>
static const double PI = 3.14159265358979323846;
double vulture_window_weight(enum VultureWindow w, size_t i, size_t n) {
    if (n < 2 || w == VULTURE_WINDOW_RECTANGULAR) return 1.0;
    double x = 2.0 * PI * (double)i / (double)(n - 1);
    return w == VULTURE_WINDOW_HAMMING ? 0.54 - 0.46 * cos(x) : 0.5 - 0.5 * cos(x);
}
void vulture_iq_apply_window(VultureIQSeries *s, enum VultureWindow w) {
    if (!s) return;
    for (size_t i = 0; i < s->size; ++i) { double x = vulture_window_weight(w, i, s->size); s->data[i].i *= x; s->data[i].q *= x; }
}

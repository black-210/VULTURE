#include "vulture_iq_spectrum.h"
#include <math.h>
static const double PI = 3.14159265358979323846;
int vulture_iq_dft_peak(const VultureIQSeries *s, double rate, VulturePeak *p) {
    if (!s || !p || !s->size || !isfinite(rate) || rate <= 0 || s->size > 4096) return -1;
    p->magnitude = -1;
    for (size_t k = 0; k <= s->size / 2; ++k) { double re = 0, im = 0;
        for (size_t n = 0; n < s->size; ++n) { double a = -2 * PI * k * n / s->size; double ci = cos(a), si = sin(a); re += s->data[n].i * ci - s->data[n].q * si; im += s->data[n].i * si + s->data[n].q * ci; }
        double m = hypot(re, im); if (m > p->magnitude) { p->magnitude = m; p->bin = k; }
    }
    p->frequency_hz = (double)p->bin * rate / s->size; return 0;
}
int vulture_iq_dft_spectrum(const VultureIQSeries *s, double rate, VultureSpectrum *spec) {
    if (!s || !spec || !s->size || !isfinite(rate) || rate <= 0 || s->size > 4096) return -1;
    spec->size = s->size / 2 + 1; spec->rate = rate; spec->data = malloc(spec->size * sizeof(VultureSpectrumBin)); if (!spec->data) return -1;
    for (size_t k = 0; k < spec->size; ++k) { double re = 0, im = 0;
        for (size_t n = 0; n < s->size; ++n) { double a = -2 * PI * k * n / s->size; double ci = cos(a), si = sin(a); re += s->data[n].i * ci - s->data[n].q * si; im += s->data[n].i * si + s->data[n].q * ci; }
        spec->data[k].magnitude = hypot(re, im); spec->data[k].frequency_hz = (double)k * rate / s->size;
    }
    return 0;
}
void vulture_iq_spectrum_free(VultureSpectrum *spec) { free(spec->data); }{
    if (spec) {
        free(spec->data);
        spec->data = NULL;
        spec->size = 0;
        spec->rate = 0.0;
    }
     return 0;
}
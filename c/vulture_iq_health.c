#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double mag(const VultureIQ *sample) { return hypot(sample->i, sample->q); }

int vulture_iq_health_clipping(const VultureIQBuffer *buffer, double limit, double *ratio) {
    size_t index;
    size_t clipped = 0;
    if (!buffer || !buffer->samples || !buffer->count || !ratio || limit <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) if (fabs(buffer->samples[index].i) >= limit || fabs(buffer->samples[index].q) >= limit) ++clipped;
    *ratio = (double)clipped / (double)buffer->count;
    return 0;
}

int vulture_iq_health_dc(const VultureIQBuffer *buffer, double *i, double *q, double *magnitude) {
    double sum_i = 0.0;
    double sum_q = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !i || !q || !magnitude) return -1;
    for (index = 0; index < buffer->count; ++index) { sum_i += buffer->samples[index].i; sum_q += buffer->samples[index].q; }
    *i = sum_i / (double)buffer->count;
    *q = sum_q / (double)buffer->count;
    *magnitude = hypot(*i, *q);
    return 0;
}

int vulture_iq_health_iq_balance(const VultureIQBuffer *buffer, double *imbalance_db, double *correlation) {
    double ii = 0.0, qq = 0.0, cross = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !imbalance_db || !correlation) return -1;
    for (index = 0; index < buffer->count; ++index) { double i = buffer->samples[index].i; double q = buffer->samples[index].q; ii += i * i; qq += q * q; cross += i * q; }
    *imbalance_db = ii > 0.0 && qq > 0.0 ? 10.0 * log10(ii / qq) : 0.0;
    *correlation = ii > 0.0 && qq > 0.0 ? cross / sqrt(ii * qq) : 0.0;
    return 0;
}

int vulture_iq_health_papr(const VultureIQBuffer *buffer, double *papr_db) {
    double peak = 0.0;
    double power = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !papr_db) return -1;
    for (index = 0; index < buffer->count; ++index) { double value = mag(&buffer->samples[index]); double p = value * value; if (p > peak) peak = p; power += p; }
    power /= (double)buffer->count;
    *papr_db = power > 0.0 ? 10.0 * log10(peak / power) : 0.0;
    return 0;
}

int vulture_iq_health_finite(const VultureIQBuffer *buffer) {
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count) return -1;
    for (index = 0; index < buffer->count; ++index) if (!isfinite(buffer->samples[index].i) || !isfinite(buffer->samples[index].q)) return -1;
    return 0;
}

#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double magnitude_at(const VultureIQ *sample) { return hypot(sample->i, sample->q); }

int vulture_iq_occupancy_ratio(const VultureIQBuffer *buffer, double threshold, double *ratio) {
    size_t index;
    size_t active = 0;
    if (!buffer || !buffer->samples || !buffer->count || !ratio || !isfinite(threshold) || threshold < 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) if (magnitude_at(&buffer->samples[index]) >= threshold) ++active;
    *ratio = (double)active / (double)buffer->count;
    return 0;
}

int vulture_iq_occupancy_auto(const VultureIQBuffer *buffer, double multiplier, double *ratio, double *threshold) {
    double sum = 0.0;
    double sum_sq = 0.0;
    double mean;
    double variance;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !ratio || !threshold || multiplier <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) { double value = magnitude_at(&buffer->samples[index]); sum += value; sum_sq += value * value; }
    mean = sum / (double)buffer->count;
    variance = fmax(0.0, sum_sq / (double)buffer->count - mean * mean);
    *threshold = mean + multiplier * sqrt(variance);
    return vulture_iq_occupancy_ratio(buffer, *threshold, ratio);
}

int vulture_iq_occupancy_histogram(const VultureIQBuffer *buffer, double max_magnitude, size_t bins, size_t *histogram) {
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !bins || !histogram || max_magnitude <= 0.0) return -1;
    for (index = 0; index < bins; ++index) histogram[index] = 0;
    for (index = 0; index < buffer->count; ++index) {
        double value = magnitude_at(&buffer->samples[index]);
        size_t bin = (size_t)(value / max_magnitude * (double)bins);
        if (bin >= bins) bin = bins - 1U;
        ++histogram[bin];
    }
    return 0;
}

int vulture_iq_occupancy_percentile(const VultureIQBuffer *buffer, double percentile, double *value) {
    double minimum = HUGE_VAL;
    double maximum = 0.0;
    size_t pass;
    if (!buffer || !buffer->samples || !buffer->count || !value || percentile < 0.0 || percentile > 1.0) return -1;
    for (pass = 0; pass < 32U; ++pass) {
        double candidate = minimum == HUGE_VAL ? 1.0 : minimum + (maximum - minimum) * (double)pass / 31.0;
        size_t below = 0;
        size_t index;
        for (index = 0; index < buffer->count; ++index) if (magnitude_at(&buffer->samples[index]) <= candidate) ++below;
        if ((double)below / (double)buffer->count >= percentile) { *value = candidate; return 0; }
        if (minimum == HUGE_VAL) minimum = 0.0;
        maximum = fmax(maximum, candidate * 2.0);
    }
    *value = maximum;
    return 0;
}

int vulture_iq_occupancy_valid(const VultureIQBuffer *buffer) { return buffer && buffer->samples && buffer->count ? 0 : -1; }

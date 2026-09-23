#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double magnitude(const VultureIQ *sample) { return hypot(sample->i, sample->q); }

int vulture_iq_burst_count(const VultureIQBuffer *buffer, double threshold, size_t *count) {
    size_t index;
    int active = 0;
    if (!buffer || !buffer->samples || !buffer->count || !count || threshold < 0.0) return -1;
    *count = 0;
    for (index = 0; index < buffer->count; ++index) {
        int now = magnitude(&buffer->samples[index]) >= threshold;
        if (now && !active) ++(*count);
        active = now;
    }
    return 0;
}

int vulture_iq_burst_duration(const VultureIQBuffer *buffer, double threshold, double sample_rate, double *mean_seconds, double *max_seconds) {
    size_t index;
    size_t current = 0;
    size_t bursts = 0;
    size_t longest = 0;
    size_t total = 0;
    if (!buffer || !buffer->samples || !buffer->count || !mean_seconds || !max_seconds || threshold < 0.0 || sample_rate <= 0.0) return -1;
    for (index = 0; index <= buffer->count; ++index) {
        int active = index < buffer->count && magnitude(&buffer->samples[index]) >= threshold;
        if (active) ++current;
        if (!active && current) { total += current; if (current > longest) longest = current; ++bursts; current = 0; }
    }
    *mean_seconds = bursts ? (double)total / (double)bursts / sample_rate : 0.0;
    *max_seconds = (double)longest / sample_rate;
    return 0;
}

int vulture_iq_burst_duty_cycle(const VultureIQBuffer *buffer, double threshold, double *duty) {
    size_t index;
    size_t active = 0;
    if (!buffer || !buffer->samples || !buffer->count || !duty || threshold < 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) if (magnitude(&buffer->samples[index]) >= threshold) ++active;
    *duty = (double)active / (double)buffer->count;
    return 0;
}

int vulture_iq_burst_edges(const VultureIQBuffer *buffer, double threshold, size_t *rising, size_t *falling) {
    size_t index;
    int previous = 0;
    if (!buffer || !buffer->samples || !buffer->count || !rising || !falling || threshold < 0.0) return -1;
    *rising = 0; *falling = 0;
    for (index = 0; index < buffer->count; ++index) {
        int current = magnitude(&buffer->samples[index]) >= threshold;
        if (current && !previous) ++(*rising);
        if (!current && previous) ++(*falling);
        previous = current;
    }
    return 0;
}

int vulture_iq_burst_threshold(const VultureIQBuffer *buffer, double factor, double *threshold) {
    double sum = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !threshold || factor <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) sum += magnitude(&buffer->samples[index]);
    *threshold = factor * sum / (double)buffer->count;
    return isfinite(*threshold) ? 0 : -1;
}

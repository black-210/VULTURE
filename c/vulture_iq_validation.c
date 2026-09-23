#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>
#include <stdio.h>

static double iq_mag(const VultureIQ *sample) {
    return sample ? hypot(sample->i, sample->q) : 0.0;
}

static double iq_mean_i(const VultureIQBuffer *buffer) {
    double sum = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count) return 0.0;
    for (index = 0; index < buffer->count; ++index) sum += buffer->samples[index].i;
    return sum / (double)buffer->count;
}

static double iq_mean_q(const VultureIQBuffer *buffer) {
    double sum = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count) return 0.0;
    for (index = 0; index < buffer->count; ++index) sum += buffer->samples[index].q;
    return sum / (double)buffer->count;
}

static double iq_mean_power(const VultureIQBuffer *buffer) {
    double sum = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count) return 0.0;
    for (index = 0; index < buffer->count; ++index) sum += iq_mag(&buffer->samples[index]) * iq_mag(&buffer->samples[index]);
    return sum / (double)buffer->count;
}

static double iq_variance_component(const VultureIQBuffer *buffer, int quadrature) {
    double mean;
    double sum = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count) return 0.0;
    mean = quadrature ? iq_mean_q(buffer) : iq_mean_i(buffer);
    for (index = 0; index < buffer->count; ++index) {
        double value = quadrature ? buffer->samples[index].q : buffer->samples[index].i;
        double delta = value - mean;
        sum += delta * delta;
    }
    return sum / (double)buffer->count;
}

int vulture_iq_validate_numeric(const VultureIQBuffer *buffer, double max_abs) {
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !isfinite(max_abs) || max_abs <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) {
        double i = buffer->samples[index].i;
        double q = buffer->samples[index].q;
        if (!isfinite(i) || !isfinite(q)) return -1;
        if (fabs(i) > max_abs || fabs(q) > max_abs) return -1;
    }
    return 0;
}

int vulture_iq_validate_quality(const VultureIQBuffer *buffer, double *dc_i, double *dc_q, double *power, double *variance) {
    if (!buffer || !dc_i || !dc_q || !power || !variance) return -1;
    if (!buffer->samples || !buffer->count) return -1;
    *dc_i = iq_mean_i(buffer);
    *dc_q = iq_mean_q(buffer);
    *power = iq_mean_power(buffer);
    *variance = iq_variance_component(buffer, 0) + iq_variance_component(buffer, 1);
    if (!isfinite(*dc_i) || !isfinite(*dc_q) || !isfinite(*power) || !isfinite(*variance)) return -1;
    return 0;
}

int vulture_iq_validate_text_report(const VultureIQBuffer *buffer, char *out, size_t length) {
    double dc_i, dc_q, power, variance;
    if (!out || !length) return -1;
    if (vulture_iq_validate_quality(buffer, &dc_i, &dc_q, &power, &variance)) return -1;
    snprintf(out, length, "{\n  \"samples\": %zu,\n  \"dc_i\": %.12g,\n  \"dc_q\": %.12g,\n  \"mean_power\": %.12g,\n  \"variance\": %.12g\n}\n", buffer->count, dc_i, dc_q, power, variance);
    return 0;
}

int vulture_iq_validate_sample_rate(double sample_rate) {
    return isfinite(sample_rate) && sample_rate > 0.0 && sample_rate <= 1.0e12 ? 0 : -1;
}

int vulture_iq_validate_text_limits(const VultureIQBuffer *buffer) {
    return buffer && buffer->count > 0 && buffer->count <= 10000000U ? 0 : -1;
}

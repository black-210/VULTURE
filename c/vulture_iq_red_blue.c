#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double squared(double value) { return value * value; }

int vulture_iq_red_features(const VultureIQBuffer *buffer, double sample_rate, double *anomaly_score, double *burst_score, double *spectral_score) {
    double sum = 0.0;
    double square = 0.0;
    double peak = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !anomaly_score || !burst_score || !spectral_score || sample_rate <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) { double value = hypot(buffer->samples[index].i, buffer->samples[index].q); sum += value; square += squared(value); if (value > peak) peak = value; }
    *anomaly_score = peak / fmax(1e-12, sqrt(square / (double)buffer->count));
    *burst_score = square / fmax(1e-12, sum * sum / (double)buffer->count);
    *spectral_score = fmin(1.0, fabs((double)sample_rate) / fmax(sample_rate, 1.0));
    return 0;
}

int vulture_iq_blue_features(const VultureIQBuffer *buffer, double *integrity_score, double *stability_score, double *calibration_score) {
    double dc_i = 0.0, dc_q = 0.0, power = 0.0, variance = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !integrity_score || !stability_score || !calibration_score) return -1;
    for (index = 0; index < buffer->count; ++index) { dc_i += buffer->samples[index].i; dc_q += buffer->samples[index].q; power += squared(hypot(buffer->samples[index].i, buffer->samples[index].q)); }
    dc_i /= (double)buffer->count; dc_q /= (double)buffer->count; power /= (double)buffer->count;
    for (index = 0; index < buffer->count; ++index) { double value = hypot(buffer->samples[index].i, buffer->samples[index].q); variance += squared(value - sqrt(power)); }
    variance /= (double)buffer->count;
    *integrity_score = isfinite(power) ? 1.0 : 0.0;
    *stability_score = 1.0 / (1.0 + sqrt(variance));
    *calibration_score = 1.0 / (1.0 + hypot(dc_i, dc_q));
    return 0;
}

int vulture_iq_red_blue_scores(const VultureIQBuffer *buffer, double sample_rate, double *red, double *blue) {
    double anomaly, burst, spectral, integrity, stability, calibration;
    if (!red || !blue) return -1;
    if (vulture_iq_red_features(buffer, sample_rate, &anomaly, &burst, &spectral)) return -1;
    if (vulture_iq_blue_features(buffer, &integrity, &stability, &calibration)) return -1;
    *red = (anomaly + burst + spectral) / 3.0;
    *blue = (integrity + stability + calibration) / 3.0;
    return 0;
}

int vulture_iq_red_blue_local_only(const VultureIQBuffer *buffer) { return buffer && buffer->samples && buffer->count ? 0 : -1; }

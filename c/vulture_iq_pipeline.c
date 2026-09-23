#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>
#include <stdio.h>

static int valid_rate(double rate) { return isfinite(rate) && rate > 0.0 && rate <= 1.0e12; }
static int valid_range(double low, double high) { return isfinite(low) && isfinite(high) && low <= high; }

int vulture_iq_pipeline_validate(const VultureIQBuffer *buffer, double sample_rate) {
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !valid_rate(sample_rate)) return -1;
    if (buffer->count > 10000000U) return -1;
    for (index = 0; index < buffer->count; ++index) {
        if (!isfinite(buffer->samples[index].i) || !isfinite(buffer->samples[index].q)) return -1;
    }
    return 0;
}

int vulture_iq_pipeline_band(const VultureIQBuffer *buffer, double sample_rate, double low, double high, double *fraction) {
    size_t index;
    size_t selected = 0;
    if (vulture_iq_pipeline_validate(buffer, sample_rate) || !valid_range(low, high) || !fraction) return -1;
    for (index = 0; index < buffer->count; ++index) {
        double frequency = atan2(buffer->samples[index].q, buffer->samples[index].i) * sample_rate / 6.283185307179586;
        if (frequency >= low && frequency <= high) ++selected;
    }
    *fraction = (double)selected / (double)buffer->count;
    return 0;
}

int vulture_iq_pipeline_integrity(const VultureIQBuffer *buffer, double *score) {
    size_t index;
    double bad = 0.0;
    if (!score || !buffer || !buffer->samples || !buffer->count) return -1;
    for (index = 0; index < buffer->count; ++index) {
        double magnitude = hypot(buffer->samples[index].i, buffer->samples[index].q);
        if (!isfinite(magnitude) || magnitude > 1000.0) bad += 1.0;
    }
    *score = 1.0 - bad / (double)buffer->count;
    return 0;
}

int vulture_iq_pipeline_summary(const VultureIQBuffer *buffer, double sample_rate, char *out, size_t length) {
    double integrity;
    double power = 0.0;
    double maximum = 0.0;
    size_t index;
    int written;
    if (!out || !length || vulture_iq_pipeline_validate(buffer, sample_rate)) return -1;
    if (vulture_iq_pipeline_integrity(buffer, &integrity)) return -1;
    for (index = 0; index < buffer->count; ++index) { double magnitude = hypot(buffer->samples[index].i, buffer->samples[index].q); power += magnitude * magnitude; if (magnitude > maximum) maximum = magnitude; }
    power /= (double)buffer->count;
    written = snprintf(out, length, "{\n  \"input\": \"txt-iq\",\n  \"samples\": %zu,\n  \"sample_rate_hz\": %.12g,\n  \"integrity_score\": %.12g,\n  \"mean_power\": %.12g,\n  \"peak_magnitude\": %.12g,\n  \"receive_only\": true,\n  \"network_access\": false,\n  \"transmit\": false\n}\n", buffer->count, sample_rate, integrity, power, maximum);
    return written >= 0 && (size_t)written < length ? 0 : -1;
}

int vulture_iq_pipeline_local_only(void) { return 0; }
int vulture_iq_pipeline_no_emulation(void) { return 0; }
int vulture_iq_pipeline_txt_only(void) { return 0; }
int vulture_iq_pipeline_iq_only(void) { return 0; }

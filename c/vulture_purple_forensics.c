#include "vulture_purple_forensics.h"

#include <math.h>
#include <stdio.h>

static double magnitude(const VultureIQ *sample) {
    return hypot(sample->i, sample->q);
}

int vulture_purple_forensics_from_iq(const VultureIQBuffer *buffer, double sample_rate_hz, VulturePurpleForensics *result) {
    double mean = 0.0;
    double variance = 0.0;
    double anomaly = 0.0;
    double integrity = 0.0;
    double clarity = 0.0;
    size_t index;

    if (!buffer || !buffer->samples || !buffer->count || !result || !isfinite(sample_rate_hz) || sample_rate_hz <= 0.0) {
        return -1;
    }

    for (index = 0; index < buffer->count; ++index) {
        const double mag = magnitude(&buffer->samples[index]);
        mean += mag;
    }
    mean /= (double)buffer->count;

    for (index = 0; index < buffer->count; ++index) {
        const double delta = magnitude(&buffer->samples[index]) - mean;
        variance += delta * delta;
    }
    variance /= (double)buffer->count;

    for (index = 0; index < buffer->count; ++index) {
        const double mag = magnitude(&buffer->samples[index]);
        if (mag > mean + 2.0 * sqrt(variance)) {
            anomaly += 1.0;
        }
        integrity += mag;
        clarity += 1.0 / (1.0 + fabs(buffer->samples[index].i) + fabs(buffer->samples[index].q));
    }

    result->anomaly_ratio = anomaly / (double)buffer->count;
    result->integrity_ratio = integrity / (double)buffer->count / (mean + 1e-12);
    result->clarity_ratio = clarity / (double)buffer->count;
    result->blue_score = 0.5 * result->integrity_ratio + 0.5 * result->clarity_ratio;
    result->purple_score = 0.6 * result->blue_score + 0.4 * (1.0 - result->anomaly_ratio);
    result->receive_only = 1;
    result->network_disabled = 1;
    result->transmit_disabled = 1;
    return 0;
}

int vulture_purple_forensics_report(const VulturePurpleForensics *result, char *out, size_t out_len) {
    if (!result || !out || out_len == 0) {
        return -1;
    }

    snprintf(
        out,
        out_len,
        "{\n"
        "  \"engine\": \"vulture-purple-forensics\",\n"
        "  \"blue_score\": %.12g,\n"
        "  \"purple_score\": %.12g,\n"
        "  \"anomaly_ratio\": %.12g,\n"
        "  \"integrity_ratio\": %.12g,\n"
        "  \"clarity_ratio\": %.12g,\n"
        "  \"receive_only\": %s,\n"
        "  \"network_disabled\": %s,\n"
        "  \"transmit_disabled\": %s\n"
        "}\n",
        result->blue_score,
        result->purple_score,
        result->anomaly_ratio,
        result->integrity_ratio,
        result->clarity_ratio,
        result->receive_only ? "true" : "false",
        result->network_disabled ? "true" : "false",
        result->transmit_disabled ? "true" : "false"
    );
    return 0;
}

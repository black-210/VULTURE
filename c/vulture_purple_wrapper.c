#include "vulture_purple_wrapper.h"

#include <math.h>
#include <stdio.h>

int vulture_purple_wrapper_compute(const double *values, size_t count, VulturePurpleWrapper *wrapper) {
    double sum = 0.0;
    double variance = 0.0;
    double anomaly = 0.0;
    size_t index;

    if (!values || !count || !wrapper) {
        return -1;
    }

    for (index = 0; index < count; ++index) {
        sum += values[index];
    }

    for (index = 0; index < count; ++index) {
        const double delta = values[index] - (sum / (double)count);
        variance += delta * delta;
    }
    variance /= (double)count;

    for (index = 0; index < count; ++index) {
        if (fabs(values[index] - (sum / (double)count)) > 2.0 * sqrt(variance)) {
            anomaly += 1.0;
        }
    }

    wrapper->score = 1.0 / (1.0 + sqrt(variance));
    wrapper->confidence = 1.0 - anomaly / (double)count;
    wrapper->anomaly_ratio = anomaly / (double)count;
    wrapper->receive_only = 1;
    wrapper->network_disabled = 1;
    wrapper->transmit_disabled = 1;
    return 0;
}

int vulture_purple_wrapper_report(const VulturePurpleWrapper *wrapper, char *out, size_t out_len) {
    if (!wrapper || !out || out_len == 0) {
        return -1;
    }

    snprintf(
        out,
        out_len,
        "{\n"
        "  \"engine\": \"vulture-purple-wrapper\",\n"
        "  \"score\": %.12g,\n"
        "  \"confidence\": %.12g,\n"
        "  \"anomaly_ratio\": %.12g,\n"
        "  \"receive_only\": %s,\n"
        "  \"network_disabled\": %s,\n"
        "  \"transmit_disabled\": %s\n"
        "}\n",
        wrapper->score,
        wrapper->confidence,
        wrapper->anomaly_ratio,
        wrapper->receive_only ? "true" : "false",
        wrapper->network_disabled ? "true" : "false",
        wrapper->transmit_disabled ? "true" : "false"
    );
    return 0;
}

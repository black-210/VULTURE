#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>
#include <stdio.h>

static int append(char *out, size_t length, size_t *used, const char *text) {
    int written;
    if (!out || !used || !text || *used >= length) return -1;
    written = snprintf(out + *used, length - *used, "%s", text);
    if (written < 0 || (size_t)written >= length - *used) return -1;
    *used += (size_t)written;
    return 0;
}

int vulture_iq_text_json_header(const VultureIQBuffer *buffer, double sample_rate, char *out, size_t length) {
    int written;
    if (!buffer || !buffer->samples || !buffer->count || !out || !length || sample_rate <= 0.0) return -1;
    written = snprintf(out, length, "{\n  \"engine\": \"vulture-c-local-iq\",\n  \"input_kind\": \"txt-iq\",\n  \"receive_only\": true,\n  \"network_disabled\": true,\n  \"transmit_disabled\": true,\n  \"samples\": %zu,\n  \"sample_rate_hz\": %.12g,\n  \"metrics\": {\n", buffer->count, sample_rate);
    return written >= 0 && (size_t)written < length ? 0 : -1;
}

int vulture_iq_text_json_metric(char *out, size_t length, const char *name, double value, int last) {
    int written;
    if (!out || !length || !name || !isfinite(value)) return -1;
    written = snprintf(out, length, "    \"%s\": %.12g%s\n", name, value, last ? "" : ",");
    return written >= 0 && (size_t)written < length ? 0 : -1;
}

int vulture_iq_text_json_footer(char *out, size_t length) {
    const char *footer = "  }\n}\n";
    if (!out || length < 7U) return -1;
    snprintf(out, length, "%s", footer);
    return 0;
}

int vulture_iq_text_report_summary(const VultureIQBuffer *buffer, double sample_rate, char *out, size_t length) {
    double power = 0.0;
    double peak = 0.0;
    double value;
    size_t index;
    size_t used = 0;
    char line[128];
    if (!buffer || !buffer->samples || !buffer->count || !out || !length || sample_rate <= 0.0) return -1;
    if (vulture_iq_text_json_header(buffer, sample_rate, out, length)) return -1;
    used = strlen(out);
    for (index = 0; index < buffer->count; ++index) { value = hypot(buffer->samples[index].i, buffer->samples[index].q); power += value * value; if (value > peak) peak = value; }
    power /= (double)buffer->count;
    snprintf(line, sizeof(line), "    \"mean_power\": %.12g,\n", power); if (append(out, length, &used, line)) return -1;
    snprintf(line, sizeof(line), "    \"peak_magnitude\": %.12g,\n", peak); if (append(out, length, &used, line)) return -1;
    snprintf(line, sizeof(line), "    \"rms\": %.12g\n", sqrt(power)); if (append(out, length, &used, line)) return -1;
    if (append(out, length, &used, "  }\n}\n")) return -1;
    return 0;
}

int vulture_iq_text_report_safe(const VultureIQBuffer *buffer) { return buffer && buffer->samples && buffer->count ? 0 : -1; }

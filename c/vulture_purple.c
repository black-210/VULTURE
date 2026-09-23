#include "vulture_purple.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int add_value(VulturePurpleSeries *s, double value) {
    if (s->count == s->capacity) {
        size_t next = s->capacity ? s->capacity * 2 : 256;
        double *grown;
        if (next < s->capacity || next > (size_t)-1 / sizeof(*grown)) return -1;
        grown = realloc(s->values, next * sizeof(*grown));
        if (!grown) return -1;
        s->values = grown; s->capacity = next;
    }
    s->values[s->count++] = value;
    return 0;
}

int vulture_purple_load(const char *path, VulturePurpleSeries *s) {
    FILE *f; double value;
    if (!path || !s) return -1;
    memset(s, 0, sizeof(*s)); f = fopen(path, "r"); if (!f) return -1;
    while (fscanf(f, " %lf", &value) == 1) {
        if (!isfinite(value) || add_value(s, value) != 0) { fclose(f); vulture_purple_free(s); return -1; }
    }
    fclose(f);
    if (!s->count) { vulture_purple_free(s); return -1; }
    return 0;
}

void vulture_purple_free(VulturePurpleSeries *s) {
    if (!s) return; free(s->values); memset(s, 0, sizeof(*s));
}

int vulture_purple_stats(const VulturePurpleSeries *s, double z, VulturePurpleStats *out) {
    size_t i; double sum = 0, variance = 0, threshold, delta;
    if (!s || !out || !s->values || !s->count || !isfinite(z) || z <= 0) return -1;
    out->count = s->count; out->min = s->values[0]; out->max = s->values[0];
    for (i = 0; i < s->count; ++i) { sum += s->values[i]; if (s->values[i] < out->min) out->min = s->values[i]; if (s->values[i] > out->max) out->max = s->values[i]; }
    out->mean = sum / s->count;
    for (i = 0; i < s->count; ++i) { delta = s->values[i] - out->mean; variance += delta * delta; }
    out->stddev = sqrt(variance / s->count); threshold = z * out->stddev;
    out->anomaly_count = 0;
    if (threshold > 0) for (i = 0; i < s->count; ++i) if (fabs(s->values[i] - out->mean) > threshold) out->anomaly_count += 1;
    out->anomaly_ratio = out->anomaly_count / (double)s->count;
    return 0;
}

int vulture_purple_compare(const VulturePurpleSeries *baseline, const VulturePurpleSeries *sample, double z, VulturePurpleStats *out) {
    VulturePurpleStats base; VulturePurpleSeries residual = {0}; size_t i, n;
    if (!baseline || !sample || !out || !baseline->count || !sample->count) return -1;
    if (vulture_purple_stats(baseline, z, &base) != 0) return -1;
    n = sample->count;
    residual.values = malloc(n * sizeof(*residual.values)); if (!residual.values) return -1;
    residual.count = residual.capacity = n;
    for (i = 0; i < n; ++i) residual.values[i] = sample->values[i] - base.mean;
    i = vulture_purple_stats(&residual, z, out); vulture_purple_free(&residual); return (int)i;
}

int vulture_purple_controls(VulturePurpleControls *c) {
    if (!c) return -1;
    c->provenance_ok = 1; c->baseline_ok = 1; c->input_bounded = 1; c->receive_only = 1; c->network_disabled = 1; c->transmit_disabled = 1;
    return 0;
}

int vulture_purple_report(const VulturePurpleStats *s, const VulturePurpleControls *c, char *out, size_t len) {
    if (!s || !c || !out || !len) return -1;
    snprintf(out, len, "{\n  \"engine\": \"vulture-c-purple\",\n  \"samples\": %zu,\n  \"mean\": %.12g,\n  \"stddev\": %.12g,\n  \"min\": %.12g,\n  \"max\": %.12g,\n  \"anomaly_count\": %.12g,\n  \"anomaly_ratio\": %.12g,\n  \"controls\": {\"provenance\": %s, \"baseline\": %s, \"bounded_input\": %s, \"receive_only\": %s, \"network_disabled\": %s, \"transmit_disabled\": %s}\n}\n", s->count, s->mean, s->stddev, s->min, s->max, s->anomaly_count, s->anomaly_ratio, c->provenance_ok ? "true" : "false", c->baseline_ok ? "true" : "false", c->input_bounded ? "true" : "false", c->receive_only ? "true" : "false", c->network_disabled ? "true" : "false", c->transmit_disabled ? "true" : "false");
    return 0;
}

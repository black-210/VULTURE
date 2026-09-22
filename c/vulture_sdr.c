#include "vulture_sdr.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int finite_pair(double i, double q) { return isfinite(i) && isfinite(q); }

int vulture_iq_load_text(const char *path, VultureIQBuffer *buffer) {
    FILE *file; double i, q; size_t capacity = 256;
    if (!path || !buffer) return -1;
    buffer->samples = NULL; buffer->count = 0; buffer->capacity = 0;
    file = fopen(path, "r"); if (!file) return -1;
    buffer->samples = malloc(capacity * sizeof(*buffer->samples));
    if (!buffer->samples) { fclose(file); return -1; }
    while (fscanf(file, " %lf%*[,; \t]%lf", &i, &q) == 2) {
        VultureIQ *grown;
        if (!finite_pair(i, q)) { vulture_iq_free(buffer); fclose(file); return -1; }
        if (buffer->count == capacity) {
            if (capacity > (size_t)-1 / 2) { vulture_iq_free(buffer); fclose(file); return -1; }
            grown = realloc(buffer->samples, capacity * 2 * sizeof(*grown));
            if (!grown) { vulture_iq_free(buffer); fclose(file); return -1; }
            buffer->samples = grown; capacity *= 2;
        }
        buffer->samples[buffer->count++] = (VultureIQ){i, q};
    }
    fclose(file); buffer->capacity = capacity;
    if (buffer->count == 0) { vulture_iq_free(buffer); return -1; }
    return 0;
}

void vulture_iq_free(VultureIQBuffer *buffer) {
    if (!buffer) return;
    free(buffer->samples); buffer->samples = NULL; buffer->count = 0; buffer->capacity = 0;
}

int vulture_iq_stats(const VultureIQBuffer *buffer, double sample_rate, VultureIQStats *stats) {
    size_t n, k; double sum_i = 0, sum_q = 0, power = 0, peak = 0;
    double phase_sum = 0, phase_sq = 0, cross = 0, ii = 0, qq = 0, prev_q = 0;
    if (!buffer || !stats || !buffer->samples || !buffer->count || !isfinite(sample_rate) || sample_rate <= 0) return -1;
    n = buffer->count;
    for (k = 0; k < n; ++k) {
        double i = buffer->samples[k].i, q = buffer->samples[k].q;
        double mag = hypot(i, q), phase = atan2(q, i);
        sum_i += i; sum_q += q; power += mag * mag; if (mag > peak) peak = mag;
        phase_sum += phase; phase_sq += phase * phase; ii += i * i; qq += q * q; cross += i * q;
    }
    stats->count = n; stats->sample_rate = sample_rate; stats->dc_i = sum_i / n; stats->dc_q = sum_q / n;
    stats->mean_power = power / n; stats->rms = sqrt(stats->mean_power); stats->peak = peak;
    stats->crest_factor = stats->rms > 0 ? peak / stats->rms : 0;
    stats->phase_mean = phase_sum / n;
    stats->phase_stddev = sqrt(fmax(0.0, phase_sq / n - stats->phase_mean * stats->phase_mean));
    stats->occupied_bandwidth_hz = sample_rate * fmin(1.0, stats->rms > 0 ? (2.0 * stats->phase_stddev / M_PI) : 0.0);
    stats->zero_crossing_rate = 0;
    for (k = 1; k < n; ++k) if ((buffer->samples[k - 1].q < 0) != (buffer->samples[k].q < 0)) stats->zero_crossing_rate += 1.0;
    stats->zero_crossing_rate /= (double)(n - (n > 1));
    stats->frequency_estimate_hz = stats->zero_crossing_rate * sample_rate / 2.0;
    stats->iq_gain_imbalance_db = (ii > 0 && qq > 0) ? 10.0 * log10(ii / qq) : 0;
    stats->iq_correlation = (ii > 0 && qq > 0) ? cross / sqrt(ii * qq) : 0;
    (void)prev_q;
    return 0;
}

int vulture_iq_report(const VultureIQStats *s, char *out, size_t len) {
    if (!s || !out || !len) return -1;
    snprintf(out, len, "{\n  \"engine\": \"vulture-c-sdr\",\n  \"samples\": %zu,\n  \"sample_rate_hz\": %.12g,\n  \"dc_i\": %.12g,\n  \"dc_q\": %.12g,\n  \"rms\": %.12g,\n  \"peak\": %.12g,\n  \"mean_power\": %.12g,\n  \"crest_factor\": %.12g,\n  \"phase_mean_rad\": %.12g,\n  \"phase_stddev_rad\": %.12g,\n  \"occupied_bandwidth_hz\": %.12g,\n  \"zero_crossing_rate\": %.12g,\n  \"frequency_estimate_hz\": %.12g,\n  \"iq_gain_imbalance_db\": %.12g,\n  \"iq_correlation\": %.12g,\n  \"status\": \"receive-only-local-analysis\"\n}\n", s->count, s->sample_rate, s->dc_i, s->dc_q, s->rms, s->peak, s->mean_power, s->crest_factor, s->phase_mean, s->phase_stddev, s->occupied_bandwidth_hz, s->zero_crossing_rate, s->frequency_estimate_hz, s->iq_gain_imbalance_db, s->iq_correlation);
    return 0;
}

#include "vulture_sdr.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int finite_pair(double i, double q) { return isfinite(i) && isfinite(q); }

static int load_interleaved_pairs(const char *path, VultureIQBuffer *buffer) {
    FILE *file; double i, q; size_t capacity = 256;
    if (!path || !buffer) return -1;
    buffer->samples = NULL; buffer->count = 0; buffer->capacity = 0;
    file = fopen(path, "r");
    if (!file) return -1;
    buffer->samples = malloc(capacity * sizeof(*buffer->samples));
    if (!buffer->samples) {
        fclose(file);
        return -1;
    }
    while (fscanf(file, " %lf%*[,; \t]%lf", &i, &q) == 2) {
        VultureIQ *grown;
        if (!finite_pair(i, q)) {
            vulture_iq_free(buffer);
            fclose(file);
            return -1;
        }
        if (buffer->count == capacity) {
            if (capacity > (size_t)-1 / 2) {
                vulture_iq_free(buffer);
                fclose(file);
                return -1;
            }
            grown = realloc(buffer->samples, capacity * 2 * sizeof(*grown));
            if (!grown) {
                vulture_iq_free(buffer);
                fclose(file);
                return -1;
            }
            buffer->samples = grown;
            capacity *= 2;
        }
        buffer->samples[buffer->count++] = (VultureIQ){i, q};
    }
    fclose(file);
    buffer->capacity = capacity;
    if (buffer->count == 0) {
        vulture_iq_free(buffer);
        return -1;
    }
    return 0;
}

int vulture_iq_load_text(const char *path, VultureIQBuffer *buffer) {
    return load_interleaved_pairs(path, buffer);
}

int vulture_iq_load_complex_file(const char *path, VultureIQBuffer *buffer) {
    return load_interleaved_pairs(path, buffer);
}

int vulture_iq_load_iq_file(const char *path, VultureIQBuffer *buffer) {
    return load_interleaved_pairs(path, buffer);
}

void vulture_iq_free(VultureIQBuffer *buffer) {
    if (!buffer) return;
    free(buffer->samples);
    buffer->samples = NULL;
    buffer->count = 0;
    buffer->capacity = 0;
}

int vulture_iq_stats(const VultureIQBuffer *buffer, double sample_rate, VultureIQStats *stats) {
    size_t n, k; double sum_i = 0, sum_q = 0, power = 0, peak = 0;
    double phase_sum = 0, phase_sq = 0, cross = 0, ii = 0, qq = 0;
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
    return 0;
}

int vulture_iq_report(const VultureIQStats *s, char *out, size_t len) {
    if (!s || !out || !len) return -1;
    snprintf(
        out, len,
        "{\n"
        "  \"engine\": \"vulture-c-sdr\",\n"
        "  \"samples\": %zu,\n"
        "  \"sample_rate_hz\": %.12g,\n"
        "  \"dc_i\": %.12g,\n"
        "  \"dc_q\": %.12g,\n"
        "  \"rms\": %.12g,\n"
        "  \"peak\": %.12g,\n"
        "  \"mean_power\": %.12g,\n"
        "  \"crest_factor\": %.12g,\n"
        "  \"phase_mean\": %.12g,\n"
        "  \"phase_stddev\": %.12g,\n"
        "  \"occupied_bandwidth_hz\": %.12g,\n"
        "  \"frequency_estimate_hz\": %.12g,\n"
        "  \"iq_gain_imbalance_db\": %.12g,\n"
        "  \"iq_correlation\": %.12g\n"
        "}\n",
        s->count,
        s->sample_rate,
        s->dc_i,
        s->dc_q,
        s->rms,
        s->peak,
        s->mean_power,
        s->crest_factor,
        s->phase_mean,
        s->phase_stddev,
        s->occupied_bandwidth_hz,
        s->frequency_estimate_hz,
        s->iq_gain_imbalance_db,
        s->iq_correlation);
    return 0;
}

int vulture_sdr_red_blue_features(const VultureIQBuffer *buffer, double sample_rate, VultureSDRFeatureSet *features) {
    VultureIQStats stats;
    double dc_mag;
    double sum_abs = 0.0, clipping = 0.0, threshold = 0.0;
    size_t k;
    if (!buffer || !features || !buffer->samples || !buffer->count || !isfinite(sample_rate) || sample_rate <= 0) return -1;
    if (vulture_iq_stats(buffer, sample_rate, &stats) != 0) return -1;

    dc_mag = hypot(stats.dc_i, stats.dc_q);
    threshold = stats.rms > 0 ? 3.0 * stats.rms : 0.0;
    for (k = 0; k < buffer->count; ++k) {
        double mag = hypot(buffer->samples[k].i, buffer->samples[k].q);
        sum_abs += mag;
        if (mag > threshold) clipping += 1.0;
    }
    clipping /= (double)buffer->count;

    features->red_score = stats.phase_stddev + stats.zero_crossing_rate + stats.occupied_bandwidth_hz / fmax(1.0, sample_rate) + (stats.rms > 0 ? stats.peak / stats.rms : 0.0);
    features->blue_score = 1.0 / (1.0 + dc_mag + clipping + fmax(0.0, stats.phase_mean));
    features->occupancy_ratio = stats.rms > 0 ? (stats.peak / stats.rms) : 0.0;
    features->clipping_ratio = clipping;
    features->noise_floor = stats.rms > 0 ? stats.rms / sqrt((double)buffer->count) : 0.0;
    features->spectral_centroid_hz = stats.frequency_estimate_hz;
    features->burst_ratio = stats.zero_crossing_rate;
    features->stability_index = 1.0 / (1.0 + fmax(0.0, dc_mag) + clipping + fabs(stats.phase_stddev));
    return 0;
}

int vulture_sdr_discovery_status(char *output, size_t output_len) {
    if (!output || !output_len) return -1;
    snprintf(
        output,
        output_len,
        "{\n"
        "  \"mode\": \"offline-deterministic\",\n"
        "  \"local_npz\": true,\n"
        "  \"simulator\": true,\n"
        "  \"soapy_available\": false,\n"
        "  \"device_count\": 0,\n"
        "  \"network_probe\": false,\n"
        "  \"transmit\": false,\n"
        "  \"receive_only\": true,\n"
        "  \"discovery\": \"explicit-only\"\n"
        "}\n");
    return 0;
}

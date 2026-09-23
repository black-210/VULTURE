#include "vulture_sdr.h"
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Implemented by vulture_iq_partition.c; the shared file is complex64 LE. */
int vulture_iq_read_complex64(const char *path, VultureIQBuffer *buffer);

static void usage(const char *name) {
    printf("Usage:\n");
    printf("  %s iq validate FILE.iq\n", name);
    printf("  %s iq stats FILE.iq --sample-rate HZ\n", name);
    printf("  %s sdr status\n", name);
    puts("Receive-only local IQ inspection. No transmit, discovery, scanning, or network access.");
}

static int parse_rate(const char *text, double *rate) {
    char *end = NULL;
    errno = 0;
    *rate = strtod(text, &end);
    return errno || !end || *end || !isfinite(*rate) || *rate <= 0;
}

static int load_iq(const char *path, VultureIQBuffer *buffer) {
    const char *suffix = strrchr(path, '.');
    if (!suffix || strcmp(suffix, ".iq") != 0) {
        fprintf(stderr, "input must use the canonical .iq extension\n");
        return -1;
    }
    return vulture_iq_read_complex64(path, buffer);
}

static void print_stats(const VultureIQBuffer *buffer, double rate) {
    size_t k;
    double sum_i = 0, sum_q = 0, power = 0, peak = 0;
    double phase_sum = 0, phase_sq = 0;
    for (k = 0; k < buffer->count; ++k) {
        const double i = buffer->samples[k].i;
        const double q = buffer->samples[k].q;
        const double magnitude = hypot(i, q);
        const double phase = atan2(q, i);
        sum_i += i; sum_q += q; power += magnitude * magnitude;
        if (magnitude > peak) peak = magnitude;
        phase_sum += phase; phase_sq += phase * phase;
    }
    {
        const double mean_power = power / (double)buffer->count;
        const double rms = sqrt(mean_power);
        const double phase_mean = phase_sum / (double)buffer->count;
        double crossings = 0;
        for (k = 1; k < buffer->count; ++k)
            if ((buffer->samples[k - 1].q < 0) != (buffer->samples[k].q < 0)) crossings += 1;
        printf("{\n");
        printf("  \"format\": \"complex64-le\",\n");
        printf("  \"samples\": %zu,\n", buffer->count);
        printf("  \"sample_rate_hz\": %.12g,\n", rate);
        printf("  \"duration_s\": %.12g,\n", buffer->count / rate);
        printf("  \"mean_i\": %.12g,\n", sum_i / (double)buffer->count);
        printf("  \"mean_q\": %.12g,\n", sum_q / (double)buffer->count);
        printf("  \"rms\": %.12g,\n", rms);
        printf("  \"peak\": %.12g,\n", peak);
        printf("  \"mean_power\": %.12g,\n", mean_power);
        printf("  \"crest_factor\": %.12g,\n", rms > 0 ? peak / rms : 0.0);
        printf("  \"phase_mean_rad\": %.12g,\n", phase_mean);
        printf("  \"phase_variance_rad2\": %.12g,\n", fmax(0.0, phase_sq / buffer->count - phase_mean * phase_mean));
        printf("  \"zero_crossing_rate\": %.12g,\n", buffer->count > 1 ? crossings / (buffer->count - 1) : 0.0);
        printf("  \"status\": \"receive-only-local-analysis\"\n");
        printf("}\n");
    }
}

int main(int argc, char **argv) {
    VultureIQBuffer buffer = {0};
    double rate;
    int rc;
    if (argc == 2 && (!strcmp(argv[1], "help") || !strcmp(argv[1], "--help"))) { usage(argv[0]); return 0; }
    if (argc == 3 && !strcmp(argv[1], "sdr") && !strcmp(argv[2], "status")) {
        puts("{\"receive_only\":true,\"hardware_opened\":false,\"network\":false,\"transmit\":false}");
        return 0;
    }
    if (argc == 4 && !strcmp(argv[1], "iq") && !strcmp(argv[2], "validate")) {
        rc = load_iq(argv[3], &buffer);
        if (!rc) { printf("valid complex64 IQ capture: %zu samples\n", buffer.count); vulture_iq_free(&buffer); }
        return rc ? 1 : 0;
    }
    if (argc == 6 && !strcmp(argv[1], "iq") && !strcmp(argv[2], "stats") && !strcmp(argv[4], "--sample-rate")) {
        if (parse_rate(argv[5], &rate) || load_iq(argv[3], &buffer)) { usage(argv[0]); vulture_iq_free(&buffer); return 2; }
        print_stats(&buffer, rate); vulture_iq_free(&buffer); return 0;
    }
    usage(argv[0]);
    return 2;
}

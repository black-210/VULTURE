#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    double mean_i;
    double mean_q;
    double rms_i;
    double rms_q;
    double peak_i;
    double peak_q;
    double dc_offset_i;
    double dc_offset_q;
    double power;
    double iq_imbalance_db;
    double phase_imbalance_deg;
    double skew;
    double kurtosis;
    double sample_rate_hz;
    size_t count;
} IQStats;

typedef struct {
    double *i;
    double *q;
    size_t count;
} IQBuffer;

static void print_usage(const char *program_name) {
    printf("Usage:\n");
    printf("  %s <input_iq.txt|input_iq.bin> [sample_rate_hz]\n", program_name);
    printf("\n");
    printf("Offline IQ analysis only. No transmit, no hardware probing, no SDR acquire path.\n");
}

static int load_text_iq(const char *path, IQBuffer *buffer) {
    FILE *fp = fopen(path, "r");
    char line[512];
    double a = 0.0;
    double b = 0.0;
    size_t cap = 1024;
    size_t count = 0;

    if (fp == NULL) {
        return -1;
    }

    buffer->i = (double *)malloc(cap * sizeof(double));
    buffer->q = (double *)malloc(cap * sizeof(double));
    if (buffer->i == NULL || buffer->q == NULL) {
        fclose(fp);
        return -1;
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        if (sscanf(line, "%lf %lf", &a, &b) == 2) {
            if (count == cap) {
                cap *= 2;
                buffer->i = (double *)realloc(buffer->i, cap * sizeof(double));
                buffer->q = (double *)realloc(buffer->q, cap * sizeof(double));
                if (buffer->i == NULL || buffer->q == NULL) {
                    fclose(fp);
                    return -1;
                }
            }
            buffer->i[count] = a;
            buffer->q[count] = b;
            count++;
        }
    }

    fclose(fp);
    buffer->count = count;
    return (count > 0) ? 0 : -1;
}

static int load_bin_iq(const char *path, IQBuffer *buffer) {
    FILE *fp = fopen(path, "rb");
    size_t cap = 8192;
    size_t count = 0;
    double value = 0.0;

    if (fp == NULL) {
        return -1;
    }

    buffer->i = (double *)malloc(cap * sizeof(double));
    buffer->q = (double *)malloc(cap * sizeof(double));
    if (buffer->i == NULL || buffer->q == NULL) {
        fclose(fp);
        return -1;
    }

    while (fread(&value, sizeof(double), 1, fp) == 1) {
        if (count == cap) {
            cap *= 2;
            buffer->i = (double *)realloc(buffer->i, cap * sizeof(double));
            buffer->q = (double *)realloc(buffer->q, cap * sizeof(double));
            if (buffer->i == NULL || buffer->q == NULL) {
                fclose(fp);
                return -1;
            }
        }
        buffer->i[count] = value;
        buffer->q[count] = value;
        count++;
    }

    fclose(fp);
    buffer->count = count;
    return (count > 0) ? 0 : -1;
}

static void free_iq(IQBuffer *buffer) {
    if (buffer == NULL) {
        return;
    }
    free(buffer->i);
    free(buffer->q);
    buffer->i = NULL;
    buffer->q = NULL;
    buffer->count = 0;
}

static void compute_stats(IQBuffer *buffer, IQStats *stats) {
    double sum_i = 0.0, sum_q = 0.0;
    double sum2_i = 0.0, sum2_q = 0.0;
    double max_i = -INFINITY, max_q = -INFINITY;
    double min_i = INFINITY, min_q = INFINITY;
    double corr = 0.0;
    double mean_i, mean_q, rms_i, rms_q;
    double variance_i, variance_q;
    double m3_i = 0.0, m4_i = 0.0;
    size_t i;

    memset(stats, 0, sizeof(*stats));
    if (buffer->count == 0) {
        return;
    }

    for (i = 0; i < buffer->count; ++i) {
        const double xi = buffer->i[i];
        const double xq = buffer->q[i];

        sum_i += xi;
        sum_q += xq;
        sum2_i += xi * xi;
        sum2_q += xq * xq;

        if (xi > max_i) max_i = xi;
        if (xq > max_q) max_q = xq;
        if (xi < min_i) min_i = xi;
        if (xq < min_q) min_q = xq;
    }

    mean_i = sum_i / (double)buffer->count;
    mean_q = sum_q / (double)buffer->count;
    rms_i = sqrt(sum2_i / (double)buffer->count);
    rms_q = sqrt(sum2_q / (double)buffer->count);

    variance_i = (sum2_i / (double)buffer->count) - (mean_i * mean_i);
    variance_q = (sum2_q / (double)buffer->count) - (mean_q * mean_q);

    for (i = 0; i < buffer->count; ++i) {
        const double dx = buffer->i[i] - mean_i;
        const double dy = buffer->q[i] - mean_q;
        corr += dx * dy;
        m3_i += dx * dx * dx;
        m4_i += dx * dx * dx * dx;
    }

    corr /= (double)buffer->count * (rms_i * rms_q + 1e-12);

    stats->mean_i = mean_i;
    stats->mean_q = mean_q;
    stats->rms_i = rms_i;
    stats->rms_q = rms_q;
    stats->peak_i = max_i;
    stats->peak_q = max_q;
    stats->dc_offset_i = mean_i;
    stats->dc_offset_q = mean_q;
    stats->power = 0.5 * (rms_i * rms_i + rms_q * rms_q);
    stats->iq_imbalance_db = 20.0 * log10((rms_i / (rms_q + 1e-12)) + 1e-12);
    stats->phase_imbalance_deg = asin(fmax(-1.0, fmin(1.0, corr))) * 180.0 / M_PI;
    stats->skew = (m3_i / (pow(rms_i, 3.0) + 1e-12)) / (double)buffer->count;
    stats->kurtosis = (m4_i / (pow(rms_i, 4.0) + 1e-12)) / (double)buffer->count;
    stats->count = buffer->count;
    stats->sample_rate_hz = 1e6;
}

static void emit_json_report(const IQStats *stats) {
    printf("{\n");
    printf("  \"count\": %zu,\n", stats->count);
    printf("  \"sample_rate_hz\": %.3f,\n", stats->sample_rate_hz);
    printf("  \"mean_i\": %.12f,\n", stats->mean_i);
    printf("  \"mean_q\": %.12f,\n", stats->mean_q);
    printf("  \"rms_i\": %.12f,\n", stats->rms_i);
    printf("  \"rms_q\": %.12f,\n", stats->rms_q);
    printf("  \"peak_i\": %.12f,\n", stats->peak_i);
    printf("  \"peak_q\": %.12f,\n", stats->peak_q);
    printf("  \"dc_offset_i\": %.12f,\n", stats->dc_offset_i);
    printf("  \"dc_offset_q\": %.12f,\n", stats->dc_offset_q);
    printf("  \"power\": %.12f,\n", stats->power);
    printf("  \"iq_imbalance_db\": %.12f,\n", stats->iq_imbalance_db);
    printf("  \"phase_imbalance_deg\": %.12f,\n", stats->phase_imbalance_deg);
    printf("  \"skew\": %.12f,\n", stats->skew);
    printf("  \"kurtosis\": %.12f,\n", stats->kurtosis);
    printf("  \"mode\": \"offline-analysis-only\"\n");
    printf("}\n");
}

int main(int argc, char **argv) {
    IQBuffer buffer = {0};
    IQStats stats;
    double sample_rate_hz = 1e6;

    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (argc >= 3) {
        char *end = NULL;
        sample_rate_hz = strtod(argv[2], &end);
        if (sample_rate_hz <= 0.0) {
            fprintf(stderr, "Invalid sample rate: %s\n", argv[2]);
            return 1;
        }
    }

    if (load_text_iq(argv[1], &buffer) == 0) {
        ;
    } else if (load_bin_iq(argv[1], &buffer) == 0) {
        ;
    } else {
        fprintf(stderr, "Unable to open IQ input: %s\n", argv[1]);
        return 1;
    }

    compute_stats(&buffer, &stats);
    stats.sample_rate_hz = sample_rate_hz;
    emit_json_report(&stats);

    free_iq(&buffer);
    return 0;
}

#include "vulture_core.h"

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    uint32_t state[8];
    uint64_t bitlen;
    unsigned char data[64];
    size_t datalen;
} VultureSHA256Ctx;

static const uint32_t k_sha256[64] = {
    0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u,
    0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
    0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u,
    0x72be5d74u, 0x80deb1feu, 0x9bdc06a7u, 0xc19bf174u,
    0xe49b69c1u, 0xefbe4786u, 0x0fc19dc6u, 0x240ca1ccu,
    0x2de92c6fu, 0x4a7484aau, 0x5cb0a9dcu, 0x76f988dau,
    0x983e5152u, 0xa831c66du, 0xb00327c8u, 0xbf597fc7u,
    0xc6e00bf3u, 0xd5a79147u, 0x06ca6351u, 0x14292967u,
    0x27b70a85u, 0x2e1b2138u, 0x4d2c6dfcu, 0x53380d13u,
    0x650a7354u, 0x766a0abbu, 0x81c2c92eu, 0x92722c85u,
    0xa2bfe8a1u, 0xa81a664bu, 0xc24b8b70u, 0xc76c51a3u,
    0xd192e819u, 0xd6990624u, 0xf40e3585u, 0x106aa070u,
    0x19a4c116u, 0x1e376c08u, 0x2748774cu, 0x34b0bcb5u,
    0x391c0cb3u, 0x4ed8aa4au, 0x5b9cca4fu, 0x682e6ff3u,
    0x748f82eeu, 0x78a5636fu, 0x84c87814u, 0x8cc70208u,
    0x90befffau, 0xa4506cebu, 0xbef9a3f7u, 0xc67178f2u
};

static uint32_t vulture_rotr32(uint32_t value, uint32_t bits) {
    return (value >> bits) | (value << (32u - bits));
}

static void vulture_sha256_transform(VultureSHA256Ctx *ctx, const unsigned char block[64]) {
    uint32_t a, b, c, d, e, f, g, h;
    uint32_t m[64];
    int i;

    for (i = 0; i < 16; ++i) {
        m[i] = ((uint32_t)block[i * 4] << 24u) |
               ((uint32_t)block[i * 4 + 1] << 16u) |
               ((uint32_t)block[i * 4 + 2] << 8u) |
               ((uint32_t)block[i * 4 + 3]);
    }

    for (i = 16; i < 64; ++i) {
        uint32_t s0 = vulture_rotr32(m[i - 15], 7) ^ vulture_rotr32(m[i - 15], 18) ^ (m[i - 15] >> 3);
        uint32_t s1 = vulture_rotr32(m[i - 2], 17) ^ vulture_rotr32(m[i - 2], 19) ^ (m[i - 2] >> 10);
        m[i] = m[i - 16] + s0 + m[i - 7] + s1;
    }

    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];
    e = ctx->state[4];
    f = ctx->state[5];
    g = ctx->state[6];
    h = ctx->state[7];

    for (i = 0; i < 64; ++i) {
        uint32_t s1 = vulture_rotr32(e, 6) ^ vulture_rotr32(e, 11) ^ vulture_rotr32(e, 25);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t temp1 = h + s1 + ch + k_sha256[i] + m[i];
        uint32_t s0 = vulture_rotr32(a, 2) ^ vulture_rotr32(a, 13) ^ vulture_rotr32(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t temp2 = s0 + maj;

        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
    ctx->state[4] += e;
    ctx->state[5] += f;
    ctx->state[6] += g;
    ctx->state[7] += h;
}

static void vulture_sha256_init(VultureSHA256Ctx *ctx) {
    ctx->state[0] = 0x6a09e667u;
    ctx->state[1] = 0xbb67ae85u;
    ctx->state[2] = 0x3c6ef372u;
    ctx->state[3] = 0xa54ff53au;
    ctx->state[4] = 0x510e527fu;
    ctx->state[5] = 0x9b05688cu;
    ctx->state[6] = 0x1f83d9abu;
    ctx->state[7] = 0x5be0cd19u;
    ctx->bitlen = 0;
    ctx->datalen = 0;
}

static void vulture_sha256_update(VultureSHA256Ctx *ctx, const unsigned char *data, size_t len) {
    size_t i;

    for (i = 0; i < len; ++i) {
        ctx->data[ctx->datalen] = data[i];
        ctx->datalen++;

        if (ctx->datalen == 64) {
            vulture_sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

static void vulture_sha256_final(VultureSHA256Ctx *ctx, unsigned char digest[32]) {
    size_t i;
    uint64_t bitlen = ctx->bitlen + (uint64_t)ctx->datalen * 8u;

    ctx->data[ctx->datalen++] = 0x80u;
    if (ctx->datalen > 56) {
        while (ctx->datalen < 64) {
            ctx->data[ctx->datalen++] = 0x00u;
        }
        vulture_sha256_transform(ctx, ctx->data);
        ctx->datalen = 0;
    }

    while (ctx->datalen < 56) {
        ctx->data[ctx->datalen++] = 0x00u;
    }

    for (i = 0; i < 8; ++i) {
        ctx->data[56 + i] = (unsigned char)(bitlen >> (8 * (7 - i)));
    }

    vulture_sha256_transform(ctx, ctx->data);

    for (i = 0; i < 8; ++i) {
        digest[i * 4] = (unsigned char)((ctx->state[i] >> 24) & 0xffu);
        digest[i * 4 + 1] = (unsigned char)((ctx->state[i] >> 16) & 0xffu);
        digest[i * 4 + 2] = (unsigned char)((ctx->state[i] >> 8) & 0xffu);
        digest[i * 4 + 3] = (unsigned char)(ctx->state[i] & 0xffu);
    }
}

static void vulture_hash_to_hex(const unsigned char digest[32], char hex_digest[65]) {
    static const char *hex = "0123456789abcdef";
    size_t i;

    for (i = 0; i < 32; ++i) {
        hex_digest[i * 2] = hex[(digest[i] >> 4) & 0x0fu];
        hex_digest[i * 2 + 1] = hex[digest[i] & 0x0fu];
    }
    hex_digest[64] = '\0';
}

static int vulture_compare_double_values(const void *left, const void *right) {
    const double a = *(const double *)left;
    const double b = *(const double *)right;
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

int vulture_load_signal_file(const char *path, VultureSignal *signal) {
    FILE *fp = fopen(path, "r");
    size_t capacity = 32;
    size_t count = 0;
    double value = 0.0;

    if (signal == NULL || path == NULL) {
        return -1;
    }

    signal->count = 0;
    signal->capacity = 0;
    signal->values = NULL;

    if (fp == NULL) {
        return -1;
    }

    signal->values = (double *)malloc(capacity * sizeof(double));
    if (signal->values == NULL) {
        fclose(fp);
        return -1;
    }

    while (fscanf(fp, "%lf", &value) == 1) {
        if (count == capacity) {
            double *resized = (double *)realloc(signal->values, capacity * 2u * sizeof(double));
            if (resized == NULL) {
                free(signal->values);
                signal->values = NULL;
                fclose(fp);
                return -1;
            }
            signal->values = resized;
            capacity *= 2u;
        }
        signal->values[count++] = value;
    }

    fclose(fp);

    if (count == 0) {
        free(signal->values);
        signal->values = NULL;
        return -1;
    }

    signal->count = count;
    signal->capacity = capacity;
    return 0;
}

void vulture_free_signal(VultureSignal *signal) {
    if (signal == NULL) {
        return;
    }
    free(signal->values);
    signal->values = NULL;
    signal->count = 0;
    signal->capacity = 0;
}

int vulture_compute_stats(const VultureSignal *signal, VultureStats *stats) {
    double sum = 0.0;
    double sum_sq = 0.0;
    double *sorted = NULL;
    size_t i;

    if (signal == NULL || stats == NULL || signal->count == 0 || signal->values == NULL) {
        return -1;
    }

    sorted = (double *)malloc(signal->count * sizeof(double));
    if (sorted == NULL) {
        return -1;
    }
    memcpy(sorted, signal->values, signal->count * sizeof(double));
    qsort(sorted, signal->count, sizeof(double), vulture_compare_double_values);

    stats->min = sorted[0];
    stats->max = sorted[signal->count - 1];
    stats->peak_to_peak = stats->max - stats->min;

    for (i = 0; i < signal->count; ++i) {
        sum += signal->values[i];
        sum_sq += signal->values[i] * signal->values[i];
    }

    stats->mean = sum / (double)signal->count;
    stats->rms = sqrt(sum_sq / (double)signal->count);

    {
        double variance_sum = 0.0;
        for (i = 0; i < signal->count; ++i) {
            double diff = signal->values[i] - stats->mean;
            variance_sum += diff * diff;
        }
        stats->variance = variance_sum / (double)signal->count;
        stats->stddev = sqrt(stats->variance);
    }

    if (signal->count % 2u == 0u) {
        stats->median = (sorted[(signal->count / 2u) - 1u] + sorted[signal->count / 2u]) / 2.0;
    } else {
        stats->median = sorted[signal->count / 2u];
    }

    free(sorted);
    return 0;
}

int vulture_find_peaks(const VultureSignal *signal, VulturePeakSummary *peaks, double threshold) {
    VultureStats stats;
    size_t i;

    if (signal == NULL || peaks == NULL) {
        return -1;
    }

    if (vulture_compute_stats(signal, &stats) != 0) {
        return -1;
    }

    peaks->count = 0;
    if (threshold <= 0.0) {
        threshold = stats.mean + stats.stddev;
    }

    for (i = 1; i + 1 < signal->count; ++i) {
        double current = signal->values[i];
        if (current >= signal->values[i - 1] && current >= signal->values[i + 1] && current >= threshold) {
            if (peaks->count < VULTURE_MAX_PEAKS) {
                peaks->indices[peaks->count] = i;
                peaks->amplitudes[peaks->count] = current;
                peaks->count++;
            }
        }
    }

    return 0;
}

void vulture_generate_report(const VultureStats *stats, const VulturePeakSummary *peaks, char *buffer, size_t buffer_len) {
    if (buffer == NULL || buffer_len == 0) {
        return;
    }

    if (stats == NULL || peaks == NULL) {
        snprintf(buffer, buffer_len, "{\n  \"status\": \"invalid\"\n}\n");
        return;
    }

    snprintf(buffer, buffer_len,
             "{\n"
             "  \"engine\": \"vulture_core\",\n"
             "  \"min\": %.12f,\n"
             "  \"max\": %.12f,\n"
             "  \"mean\": %.12f,\n"
             "  \"variance\": %.12f,\n"
             "  \"stddev\": %.12f,\n"
             "  \"rms\": %.12f,\n"
             "  \"median\": %.12f,\n"
             "  \"peak_to_peak\": %.12f,\n"
             "  \"peaks_detected\": %zu,\n"
             "  \"status\": \"stable\"\n"
             "}\n",
             stats->min,
             stats->max,
             stats->mean,
             stats->variance,
             stats->stddev,
             stats->rms,
             stats->median,
             stats->peak_to_peak,
             peaks->count);
}

int vulture_hash_file(const char *path, char hex_digest[65]) {
    FILE *fp = fopen(path, "rb");
    unsigned char chunk[4096];
    unsigned char digest[32];
    VultureSHA256Ctx ctx;
    size_t bytes_read;

    if (path == NULL || hex_digest == NULL) {
        return -1;
    }
    if (fp == NULL) {
        return -1;
    }

    vulture_sha256_init(&ctx);
    while ((bytes_read = fread(chunk, 1, sizeof(chunk), fp)) > 0) {
        vulture_sha256_update(&ctx, chunk, bytes_read);
    }

    if (ferror(fp) != 0) {
        fclose(fp);
        return -1;
    }

    fclose(fp);
    vulture_sha256_final(&ctx, digest);
    vulture_hash_to_hex(digest, hex_digest);
    return 0;
}

int vulture_hash_buffer(const unsigned char *buffer, size_t length, char hex_digest[65]) {
    unsigned char digest[32];
    VultureSHA256Ctx ctx;

    if (buffer == NULL || hex_digest == NULL) {
        return -1;
    }

    vulture_sha256_init(&ctx);
    vulture_sha256_update(&ctx, buffer, length);
    vulture_sha256_final(&ctx, digest);
    vulture_hash_to_hex(digest, hex_digest);
    return 0;
}

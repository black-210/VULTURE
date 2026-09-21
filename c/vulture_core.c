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

static const uint32_t sha256_k[64] = {
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

static uint32_t rotr32(uint32_t value, unsigned int bits) {
    return (value >> bits) | (value << (32u - bits));
}

static void sha256_transform(VultureSHA256Ctx *ctx, const unsigned char block[64]) {
    uint32_t w[64];
    uint32_t a, b, c, d, e, f, g, h;
    size_t i;

    for (i = 0; i < 16; ++i) {
        w[i] = ((uint32_t)block[i * 4] << 24) |
               ((uint32_t)block[i * 4 + 1] << 16) |
               ((uint32_t)block[i * 4 + 2] << 8) |
               (uint32_t)block[i * 4 + 3];
    }
    for (i = 16; i < 64; ++i) {
        uint32_t s0 = rotr32(w[i - 15], 7) ^ rotr32(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = rotr32(w[i - 2], 17) ^ rotr32(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }

    a = ctx->state[0]; b = ctx->state[1]; c = ctx->state[2]; d = ctx->state[3];
    e = ctx->state[4]; f = ctx->state[5]; g = ctx->state[6]; h = ctx->state[7];
    for (i = 0; i < 64; ++i) {
        uint32_t s1 = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t temp1 = h + s1 + ch + sha256_k[i] + w[i];
        uint32_t s0 = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t temp2 = s0 + maj;
        h = g; g = f; f = e; e = d + temp1; d = c; c = b; b = a; a = temp1 + temp2;
    }
    ctx->state[0] += a; ctx->state[1] += b; ctx->state[2] += c; ctx->state[3] += d;
    ctx->state[4] += e; ctx->state[5] += f; ctx->state[6] += g; ctx->state[7] += h;
}

static void sha256_init(VultureSHA256Ctx *ctx) {
    static const uint32_t initial[8] = {
        0x6a09e667u, 0xbb67ae85u, 0x3c6ef372u, 0xa54ff53au,
        0x510e527fu, 0x9b05688cu, 0x1f83d9abu, 0x5be0cd19u
    };
    memcpy(ctx->state, initial, sizeof(initial));
    ctx->bitlen = 0;
    ctx->datalen = 0;
}

static void sha256_update(VultureSHA256Ctx *ctx, const unsigned char *data, size_t length) {
    size_t i;
    for (i = 0; i < length; ++i) {
        ctx->data[ctx->datalen++] = data[i];
        if (ctx->datalen == sizeof(ctx->data)) {
            sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

static void sha256_final(VultureSHA256Ctx *ctx, unsigned char digest[32]) {
    size_t i;
    uint64_t bitlen = ctx->bitlen + (uint64_t)ctx->datalen * 8;
    ctx->data[ctx->datalen++] = 0x80u;
    if (ctx->datalen > 56) {
        while (ctx->datalen < 64) ctx->data[ctx->datalen++] = 0;
        sha256_transform(ctx, ctx->data);
        ctx->datalen = 0;
    }
    while (ctx->datalen < 56) ctx->data[ctx->datalen++] = 0;
    for (i = 0; i < 8; ++i) ctx->data[56 + i] = (unsigned char)(bitlen >> (56 - i * 8));
    sha256_transform(ctx, ctx->data);
    for (i = 0; i < 8; ++i) {
        digest[i * 4] = (unsigned char)(ctx->state[i] >> 24);
        digest[i * 4 + 1] = (unsigned char)(ctx->state[i] >> 16);
        digest[i * 4 + 2] = (unsigned char)(ctx->state[i] >> 8);
        digest[i * 4 + 3] = (unsigned char)ctx->state[i];
    }
}

static void digest_hex(const unsigned char digest[32], char output[65]) {
    static const char hex[] = "0123456789abcdef";
    size_t i;
    for (i = 0; i < 32; ++i) {
        output[i * 2] = hex[digest[i] >> 4];
        output[i * 2 + 1] = hex[digest[i] & 0x0fu];
    }
    output[64] = '\0';
}

static int compare_doubles(const void *left, const void *right) {
    double a = *(const double *)left;
    double b = *(const double *)right;
    return (a > b) - (a < b);
}

int vulture_load_signal_file(const char *path, VultureSignal *signal) {
    FILE *file;
    size_t capacity = 32, count = 0;
    double value;
    if (path == NULL || signal == NULL) return -1;
    signal->values = NULL; signal->count = 0; signal->capacity = 0;
    file = fopen(path, "r");
    if (file == NULL) return -1;
    signal->values = malloc(capacity * sizeof(*signal->values));
    if (signal->values == NULL) { fclose(file); return -1; }
    while (fscanf(file, "%lf", &value) == 1) {
        double *resized;
        if (!isfinite(value)) { vulture_free_signal(signal); fclose(file); return -1; }
        if (count == capacity) {
            if (capacity > (size_t)-1 / 2) { vulture_free_signal(signal); fclose(file); return -1; }
            resized = realloc(signal->values, capacity * 2 * sizeof(*signal->values));
            if (resized == NULL) { vulture_free_signal(signal); fclose(file); return -1; }
            signal->values = resized; capacity *= 2;
        }
        signal->values[count++] = value;
    }
    fclose(file);
    if (count == 0) { vulture_free_signal(signal); return -1; }
    signal->count = count; signal->capacity = capacity;
    return 0;
}

void vulture_free_signal(VultureSignal *signal) {
    if (signal == NULL) return;
    free(signal->values); signal->values = NULL; signal->count = 0; signal->capacity = 0;
}

int vulture_compute_stats(const VultureSignal *signal, VultureStats *stats) {
    double *sorted, sum = 0.0, sum_sq = 0.0, variance = 0.0;
    size_t i;
    if (signal == NULL || stats == NULL || signal->values == NULL || signal->count == 0) return -1;
    sorted = malloc(signal->count * sizeof(*sorted));
    if (sorted == NULL) return -1;
    memcpy(sorted, signal->values, signal->count * sizeof(*sorted));
    qsort(sorted, signal->count, sizeof(*sorted), compare_doubles);
    stats->min = sorted[0]; stats->max = sorted[signal->count - 1];
    for (i = 0; i < signal->count; ++i) { sum += signal->values[i]; sum_sq += signal->values[i] * signal->values[i]; }
    stats->mean = sum / (double)signal->count;
    for (i = 0; i < signal->count; ++i) { double d = signal->values[i] - stats->mean; variance += d * d; }
    stats->variance = variance / (double)signal->count;
    stats->stddev = sqrt(stats->variance); stats->rms = sqrt(sum_sq / (double)signal->count);
    stats->median = (signal->count % 2 == 0) ? (sorted[signal->count / 2 - 1] + sorted[signal->count / 2]) / 2.0 : sorted[signal->count / 2];
    stats->peak_to_peak = stats->max - stats->min;
    free(sorted);
    return 0;
}

int vulture_find_peaks(const VultureSignal *signal, VulturePeakSummary *peaks, double threshold) {
    VultureStats stats;
    size_t i;
    if (signal == NULL || peaks == NULL || vulture_compute_stats(signal, &stats) != 0) return -1;
    peaks->count = 0;
    if (!isfinite(threshold) || threshold <= 0.0) threshold = stats.mean + stats.stddev;
    for (i = 1; i + 1 < signal->count && peaks->count < VULTURE_MAX_PEAKS; ++i) {
        double current = signal->values[i];
        if (current >= signal->values[i - 1] && current >= signal->values[i + 1] && current >= threshold) {
            peaks->indices[peaks->count] = i;
            peaks->amplitudes[peaks->count++] = current;
        }
    }
    return 0;
}

void vulture_generate_report(const VultureStats *stats, const VulturePeakSummary *peaks, char *buffer, size_t buffer_len) {
    if (buffer == NULL || buffer_len == 0) return;
    if (stats == NULL || peaks == NULL) { snprintf(buffer, buffer_len, "{\n  \"status\": \"invalid\"\n}\n"); return; }
    snprintf(buffer, buffer_len,
        "{\n  \"engine\": \"vulture_core\",\n  \"min\": %.12f,\n  \"max\": %.12f,\n  \"mean\": %.12f,\n  \"variance\": %.12f,\n  \"stddev\": %.12f,\n  \"rms\": %.12f,\n  \"median\": %.12f,\n  \"peak_to_peak\": %.12f,\n  \"peaks_detected\": %zu,\n  \"status\": \"stable\"\n}\n",
        stats->min, stats->max, stats->mean, stats->variance, stats->stddev,
        stats->rms, stats->median, stats->peak_to_peak, peaks->count);
}

int vulture_hash_buffer(const unsigned char *buffer, size_t length, char hex_digest[65]) {
    VultureSHA256Ctx ctx;
    unsigned char digest[32];
    if (hex_digest == NULL || (buffer == NULL && length != 0)) return -1;
    sha256_init(&ctx);
    if (length != 0) sha256_update(&ctx, buffer, length);
    sha256_final(&ctx, digest); digest_hex(digest, hex_digest);
    return 0;
}

int vulture_hash_file(const char *path, char hex_digest[65]) {
    FILE *file;
    unsigned char chunk[4096];
    size_t read_count;
    VultureSHA256Ctx ctx;
    unsigned char digest[32];
    if (path == NULL || hex_digest == NULL) return -1;
    file = fopen(path, "rb");
    if (file == NULL) return -1;
    sha256_init(&ctx);
    while ((read_count = fread(chunk, 1, sizeof(chunk), file)) != 0) sha256_update(&ctx, chunk, read_count);
    if (ferror(file) != 0) { fclose(file); return -1; }
    fclose(file); sha256_final(&ctx, digest); digest_hex(digest, hex_digest);
    return 0;
}

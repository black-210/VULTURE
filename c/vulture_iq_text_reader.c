#include "vulture_sdr.h"
#include <ctype.h>
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define IQ_TEXT_MAX_SAMPLES 10000000U

static int iq_text_separator(int c) {
    return c == ',' || c == ';' || c == ':' || isspace((unsigned char)c);
}

static int iq_text_read_pair(FILE *stream, double *i, double *q) {
    int c;
    char token[128];
    size_t used = 0;
    if (!stream || !i || !q) return -1;
    while ((c = fgetc(stream)) != EOF) {
        if (!iq_text_separator(c)) break;
    }
    if (c == EOF) return 0;
    do {
        if (used + 1 >= sizeof(token)) return -1;
        token[used++] = (char)c;
        c = fgetc(stream);
    } while (c != EOF && !iq_text_separator(c));
    token[used] = '\0';
    errno = 0;
    *i = strtod(token, NULL);
    if (errno || !isfinite(*i)) return -1;
    while (c != EOF && iq_text_separator(c)) c = fgetc(stream);
    if (c == EOF) return -1;
    used = 0;
    do {
        if (used + 1 >= sizeof(token)) return -1;
        token[used++] = (char)c;
        c = fgetc(stream);
    } while (c != EOF && !iq_text_separator(c));
    token[used] = '\0';
    errno = 0;
    *q = strtod(token, NULL);
    if (errno || !isfinite(*q)) return -1;
    return 1;
}

int vulture_iq_text_read_strict(const char *path, VultureIQBuffer *out) {
    FILE *stream;
    size_t capacity = 1024;
    int result;
    double i;
    double q;
    if (!path || !out) return -1;
    memset(out, 0, sizeof(*out));
    stream = fopen(path, "rb");
    if (!stream) return -1;
    out->samples = calloc(capacity, sizeof(*out->samples));
    if (!out->samples) { fclose(stream); return -1; }
    while ((result = iq_text_read_pair(stream, &i, &q)) > 0) {
        VultureIQ *grown;
        if (out->count >= IQ_TEXT_MAX_SAMPLES) { fclose(stream); vulture_iq_free(out); return -1; }
        if (out->count == capacity) {
            if (capacity > IQ_TEXT_MAX_SAMPLES / 2U) { fclose(stream); vulture_iq_free(out); return -1; }
            capacity *= 2U;
            grown = realloc(out->samples, capacity * sizeof(*grown));
            if (!grown) { fclose(stream); vulture_iq_free(out); return -1; }
            out->samples = grown;
        }
        out->samples[out->count++] = (VultureIQ){i, q};
    }
    fclose(stream);
    if (result < 0 || out->count == 0) { vulture_iq_free(out); return -1; }
    out->capacity = capacity;
    return 0;
}

int vulture_iq_text_validate(const VultureIQBuffer *buffer) {
    size_t index;
    if (!buffer || !buffer->samples || buffer->count == 0) return -1;
    for (index = 0; index < buffer->count; ++index) {
        if (!isfinite(buffer->samples[index].i)) return -1;
        if (!isfinite(buffer->samples[index].q)) return -1;
    }
    return 0;
}

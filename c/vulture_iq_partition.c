#include "vulture_iq_partition.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int vulture_iq_read_complex64(const char *path, VultureIQBuffer *buffer) {
    FILE *file;
    float pair[2];
    size_t capacity = 256;
    if (!path || !buffer) return -1;
    memset(buffer, 0, sizeof(*buffer));
    file = fopen(path, "rb");
    if (!file) return -1;
    buffer->samples = malloc(capacity * sizeof(*buffer->samples));
    if (!buffer->samples) { fclose(file); return -1; }
    while (fread(pair, sizeof(pair), 1, file) == 1) {
        VultureIQ *grown;
        if (!isfinite(pair[0]) || !isfinite(pair[1])) { vulture_iq_partition_free(buffer); fclose(file); return -1; }
        if (buffer->count == capacity) {
            if (capacity > (size_t)-1 / 2) { vulture_iq_partition_free(buffer); fclose(file); return -1; }
            grown = realloc(buffer->samples, capacity * 2 * sizeof(*grown));
            if (!grown) { vulture_iq_partition_free(buffer); fclose(file); return -1; }
            buffer->samples = grown;
            capacity *= 2;
        }
        buffer->samples[buffer->count++] = (VultureIQ){pair[0], pair[1]};
    }
    if (ferror(file) || ftell(file) % (long)sizeof(pair) != 0 || buffer->count == 0) {
        vulture_iq_partition_free(buffer); fclose(file); return -1;
    }
    fclose(file);
    buffer->capacity = capacity;
    return 0;
}

void vulture_iq_partition_free(VultureIQBuffer *buffer) {
    if (!buffer) return;
    free(buffer->samples);
    memset(buffer, 0, sizeof(*buffer));
}

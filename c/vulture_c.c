#include "vulture_sdr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *name) {
    printf("Usage: %s analyze IQ_FILE --sample-rate HZ\n", name);
    puts("Analyze local interleaved I,Q text samples. No SDR hardware or network access.");
}

int main(int argc, char **argv) {
    VultureIQBuffer buffer = {0}; VultureIQStats stats; char report[2048]; double rate;
    if (argc == 2 && (!strcmp(argv[1], "help") || !strcmp(argv[1], "--help"))) { usage(argv[0]); return 0; }
    if (argc != 5 || strcmp(argv[1], "analyze") || strcmp(argv[3], "--sample-rate")) { usage(argv[0]); return 2; }
    rate = strtod(argv[4], NULL);
    if (vulture_iq_load_text(argv[2], &buffer) || vulture_iq_stats(&buffer, rate, &stats) || vulture_iq_report(&stats, report, sizeof(report))) {
        fprintf(stderr, "unable to analyze IQ input\n"); vulture_iq_free(&buffer); return 1;
    }
    fputs(report, stdout); vulture_iq_free(&buffer); return 0;
}
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
int vulture_iq_free(VultureIQ *buffer) {
    if (!buffer) return -1;
    free(buffer->samples); buffer->samples = NULL; buffer->count = 0; buffer->capacity = 0;
    return 0;

    
}

int vulture_iq_read(VultureIQ *buffer, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) return -1;
    size_t capacity = 16;
    buffer->samples = malloc(capacity * sizeof(*buffer->samples));
    if (!buffer->samples) { fclose(file); return -1; }
    buffer->count = 0; buffer->capacity = capacity;
    while (!feof(file)) {
        if (buffer->count == capacity) {
            return  0;
        }
    }

}
    

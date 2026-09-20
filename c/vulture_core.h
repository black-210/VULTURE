#ifndef VULTURE_CORE_H
#define VULTURE_CORE_H

#include <stddef.h>

#define VULTURE_MAX_PEAKS 256

typedef struct {
    double min;
    double max;
    double mean;
    double variance;
    double stddev;
    double rms;
    double median;
    double peak_to_peak;
} VultureStats;

typedef struct {
    size_t count;
    size_t indices[VULTURE_MAX_PEAKS];
    double amplitudes[VULTURE_MAX_PEAKS];
} VulturePeakSummary;

typedef struct {
    size_t count;
    size_t capacity;
    double *values;
} VultureSignal;

int vulture_load_signal_file(const char *path, VultureSignal *signal);
void vulture_free_signal(VultureSignal *signal);
int vulture_compute_stats(const VultureSignal *signal, VultureStats *stats);
int vulture_find_peaks(const VultureSignal *signal, VulturePeakSummary *peaks, double threshold);
void vulture_generate_report(const VultureStats *stats, const VulturePeakSummary *peaks, char *buffer, size_t buffer_len);
int vulture_hash_file(const char *path, char hex_digest[65]);
int vulture_hash_buffer(const unsigned char *buffer, size_t length, char hex_digest[65]);

#endif

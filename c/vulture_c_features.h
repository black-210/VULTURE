#ifndef VULTURE_C_FEATURES_H
#define VULTURE_C_FEATURES_H

#include <stddef.h>

#define VULTURE_FEATURES_MAX_PEAKS 256

typedef struct {
    double min;
    double max;
    double mean;
    double variance;
    double stddev;
    double rms;
    double median;
    double peak_to_peak;
} SignalStats;

typedef struct {
    size_t count;
    size_t indices[VULTURE_FEATURES_MAX_PEAKS];
    double amplitudes[VULTURE_FEATURES_MAX_PEAKS];
} PeakSummary;

typedef struct {
    size_t count;
    size_t capacity;
    double *values;
} SignalBuffer;

int vulture_load_signal_file(const char *path, SignalBuffer *signal);
void vulture_free_signal(SignalBuffer *signal);
int vulture_compute_stats(const SignalBuffer *signal, SignalStats *stats);
int vulture_find_peaks(const SignalBuffer *signal, PeakSummary *peak_summary, double threshold);
void vulture_generate_report(const SignalStats *stats, const PeakSummary *peaks, char *buffer, size_t buffer_len);
int vulture_sha256_file(const char *path, char hex_digest[65]);
int vulture_sha256_buffer(const unsigned char *buffer, size_t length, char hex_digest[65]);
int vulture_run_demo_suite(void);

#endif

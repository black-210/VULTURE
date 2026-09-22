#ifndef VULTURE_SDR_H
#define VULTURE_SDR_H

#include <stddef.h>

typedef struct { double i; double q; } VultureIQ;
typedef struct { VultureIQ *samples; size_t count; size_t capacity; } VultureIQBuffer;
typedef struct {
    size_t count; double sample_rate; double dc_i; double dc_q;
    double rms; double peak; double mean_power; double crest_factor;
    double phase_mean; double phase_stddev; double occupied_bandwidth_hz;
    double zero_crossing_rate; double frequency_estimate_hz;
    double iq_gain_imbalance_db; double iq_correlation;
} VultureIQStats;

int vulture_iq_load_text(const char *path, VultureIQBuffer *buffer);
void vulture_iq_free(VultureIQBuffer *buffer);
int vulture_iq_stats(const VultureIQBuffer *buffer, double sample_rate, VultureIQStats *stats);
int vulture_iq_report(const VultureIQStats *stats, char *output, size_t output_len);

#endif

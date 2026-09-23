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

typedef struct {
    double red_score;
    double blue_score;
    double occupancy_ratio;
    double clipping_ratio;
    double noise_floor;
    double spectral_centroid_hz;
    double burst_ratio;
    double stability_index;
} VultureSDRFeatureSet;

int vulture_iq_load_text(const char *path, VultureIQBuffer *buffer);
int vulture_iq_load_complex_file(const char *path, VultureIQBuffer *buffer);
int vulture_iq_load_iq_file(const char *path, VultureIQBuffer *buffer);
void vulture_iq_free(VultureIQBuffer *buffer);
int vulture_iq_stats(const VultureIQBuffer *buffer, double sample_rate, VultureIQStats *stats);
int vulture_iq_report(const VultureIQStats *stats, char *output, size_t output_len);
int vulture_sdr_red_blue_features(const VultureIQBuffer *buffer, double sample_rate, VultureSDRFeatureSet *features);
int vulture_sdr_discovery_status(char *output, size_t output_len);

#endif

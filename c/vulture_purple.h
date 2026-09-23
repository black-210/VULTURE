#ifndef VULTURE_PURPLE_H
#define VULTURE_PURPLE_H
#include <stddef.h>

typedef struct { double *values; size_t count; size_t capacity; } VulturePurpleSeries;
typedef struct { size_t count; double mean; double stddev; double min; double max; double anomaly_count; double anomaly_ratio; } VulturePurpleStats;
typedef struct { int provenance_ok; int baseline_ok; int input_bounded; int receive_only; int network_disabled; int transmit_disabled; } VulturePurpleControls;

int vulture_purple_load(const char *path, VulturePurpleSeries *series);
void vulture_purple_free(VulturePurpleSeries *series);
int vulture_purple_stats(const VulturePurpleSeries *series, double z_threshold, VulturePurpleStats *stats);
int vulture_purple_compare(const VulturePurpleSeries *baseline, const VulturePurpleSeries *sample, double z_threshold, VulturePurpleStats *stats);
int vulture_purple_controls(VulturePurpleControls *controls);
int vulture_purple_report(const VulturePurpleStats *stats, const VulturePurpleControls *controls, char *output, size_t output_len);
#endif

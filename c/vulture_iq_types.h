#ifndef VULTURE_IQ_TYPES_H
#define VULTURE_IQ_TYPES_H
#include <stddef.h>
typedef struct { double i; double q; } VultureIQSample;
typedef struct { VultureIQSample *data; size_t size; size_t capacity; } VultureIQSeries;
typedef struct { double min; double max; double mean; double rms; double variance; } VultureScalarStats;
void vulture_iq_series_free(VultureIQSeries *series);
#endif

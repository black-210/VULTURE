#ifndef VULTURE_IQ_SPECTRUM_H
#define VULTURE_IQ_SPECTRUM_H
#include "vulture_iq_types.h"
typedef struct { size_t bin; double frequency_hz; double magnitude; } VulturePeak;
int vulture_iq_dft_peak(const VultureIQSeries *series, double sample_rate, VulturePeak *peak);
#endif

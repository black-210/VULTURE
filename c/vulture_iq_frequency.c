#include "vulture_sdr.h"
#include "vulture_iq_features.h"
double vulture_iq_frequency_hz(const VultureIQBuffer *b,double rate) { return vulture_iq_zero_crossing_rate(b)*rate/2.0; }

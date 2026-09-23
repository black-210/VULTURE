#include "vulture_sdr.h"
#include "vulture_iq_features.h"
double vulture_iq_mean_power(const VultureIQBuffer *b) { double r=vulture_iq_rms(b);return r*r; }

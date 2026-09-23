#include "vulture_sdr.h"
#include "vulture_iq_features.h"
double vulture_iq_crest_factor(const VultureIQBuffer *b) { double r=vulture_iq_rms(b);return r>0?vulture_iq_peak(b)/r:0; }

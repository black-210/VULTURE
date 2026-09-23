#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
double vulture_iq_bandwidth_hz(const VultureIQBuffer *b,double rate) { double p=vulture_iq_rms(b);return p>0?rate:0; }

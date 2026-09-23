#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_peak(const VultureIQBuffer *b) { size_t k; double peak=0; if (!b || !b->samples) return 0; for (k=0;k<b->count;k++) { double m=hypot(b->samples[k].i,b->samples[k].q); if (m>peak) peak=m; } return peak; }
double vulture_iq_crest(const VultureIQBuffer *b) { double rms=vulture_iq_rms(b); return rms>0 ? vulture_iq_peak(b)/rms : 0; }

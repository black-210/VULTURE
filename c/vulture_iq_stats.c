#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_mean_power(const VultureIQBuffer *b) { size_t k; double s=0; if (!b || !b->samples || !b->count) return 0; for (k=0;k<b->count;k++) s += b->samples[k].i*b->samples[k].i + b->samples[k].q*b->samples[k].q; return s/(double)b->count; }
double vulture_iq_rms(const VultureIQBuffer *b) { return sqrt(vulture_iq_mean_power(b)); }

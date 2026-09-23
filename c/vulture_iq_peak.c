#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
double vulture_iq_peak(const VultureIQBuffer *b) { size_t k; double p=0,m; if(!b) return 0; for(k=0;k<b->count;k++){m=hypot(b->samples[k].i,b->samples[k].q);if(m>p)p=m;} return p; }

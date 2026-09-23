#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_phase_mean(const VultureIQBuffer *b) { size_t k; double s=0; if (!b || !b->count) return 0; for(k=0;k<b->count;k++) s+=atan2(b->samples[k].q,b->samples[k].i); return s/(double)b->count; }
double vulture_iq_phase_variance(const VultureIQBuffer *b) { size_t k; double s=0,s2=0; if (!b || !b->count) return 0; for(k=0;k<b->count;k++){double p=atan2(b->samples[k].q,b->samples[k].i);s+=p;s2+=p*p;} s/=b->count;s2/=b->count;return fmax(0,s2-s*s); }

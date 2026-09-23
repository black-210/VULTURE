#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
double vulture_iq_phase_mean(const VultureIQBuffer *b) { size_t k; double s=0; if(!b||!b->count)return 0;for(k=0;k<b->count;k++)s+=atan2(b->samples[k].q,b->samples[k].i);return s/b->count; }

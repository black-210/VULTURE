#include "vulture_sdr.h"
#include "vulture_iq_features.h"
double vulture_iq_dc_i(const VultureIQBuffer *b) { size_t k; double s=0; if(!b||!b->count)return 0;for(k=0;k<b->count;k++)s+=b->samples[k].i;return s/b->count; }
double vulture_iq_dc_q(const VultureIQBuffer *b) { size_t k; double s=0; if(!b||!b->count)return 0;for(k=0;k<b->count;k++)s+=b->samples[k].q;return s/b->count; }

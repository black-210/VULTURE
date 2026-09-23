#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
void vulture_iq_hann(VultureIQBuffer *b) { size_t k;if(!b||b->count<2)return;for(k=0;k<b->count;k++){double w=.5*(1-cos(2*M_PI*k/(b->count-1)));b->samples[k].i*=w;b->samples[k].q*=w;}}

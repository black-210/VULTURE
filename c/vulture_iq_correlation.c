#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
double vulture_iq_correlation(const VultureIQBuffer *b) { size_t k;double c=0,i=0,q=0;if(!b)return 0;for(k=0;k<b->count;k++){i+=b->samples[k].i*b->samples[k].i;q+=b->samples[k].q*b->samples[k].q;c+=b->samples[k].i*b->samples[k].q;}return i>0&&q>0?c/sqrt(i*q):0;}

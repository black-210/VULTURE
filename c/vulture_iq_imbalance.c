#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <math.h>
double vulture_iq_gain_db(const VultureIQBuffer *b) { size_t k; double i=0,q=0;if(!b)return 0;for(k=0;k<b->count;k++){i+=b->samples[k].i*b->samples[k].i;q+=b->samples[k].q*b->samples[k].q;}return i>0&&q>0?10*log10(i/q):0; }

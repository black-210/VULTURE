#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_zero_crossing_rate(const VultureIQBuffer *b) { size_t k; double crossings=0; if(!b||!b->samples||b->count<2)return 0;for(k=1;k<b->count;k++)if((b->samples[k-1].q<0)!=(b->samples[k].q<0))crossings++;return crossings/(double)(b->count-1); }
double vulture_iq_frequency_estimate(const VultureIQBuffer *b,double sample_rate) { if(sample_rate<=0)return NAN;return vulture_iq_zero_crossing_rate(b)*sample_rate/2.0; }

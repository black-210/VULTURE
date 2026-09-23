#include "vulture_sdr.h"
#include "vulture_iq_features.h"
double vulture_iq_zero_crossing_rate(const VultureIQBuffer *b) { size_t k; double n=0;if(!b||b->count<2)return 0;for(k=1;k<b->count;k++)if((b->samples[k-1].q<0)!=(b->samples[k].q<0))n++;return n/(b->count-1);}

#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_correlation(const VultureIQBuffer *b) { size_t k; double cross=0,ii=0,qq=0; if(!b||!b->samples)return 0; for(k=0;k<b->count;k++){ii+=b->samples[k].i*b->samples[k].i;qq+=b->samples[k].q*b->samples[k].q;cross+=b->samples[k].i*b->samples[k].q;} return ii>0&&qq>0?cross/sqrt(ii*qq):0; }
double vulture_iq_gain_imbalance_db(const VultureIQBuffer *b) { size_t k;double ii=0,qq=0;if(!b||!b->samples)return 0;for(k=0;k<b->count;k++){ii+=b->samples[k].i*b->samples[k].i;qq+=b->samples[k].q*b->samples[k].q;}return ii>0&&qq>0?10*log10(ii/qq):0;}

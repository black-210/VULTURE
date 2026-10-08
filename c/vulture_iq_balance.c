#include "vulture_sdr.h"
#include <math.h>

double vulture_iq_correlation(const VultureIQBuffer *b) { size_t k; double cross=0,ii=0,qq=0; if(!b||!b->samples)return 0; for(k=0;k<b->count;k++){ii+=b->samples[k].i*b->samples[k].i;qq+=b->samples[k].q*b->samples[k].q;cross+=b->samples[k].i*b->samples[k].q;} return ii>0&&qq>0?cross/sqrt(ii*qq):0; }
double vulture_iq_gain_imbalance_db(const VultureIQBuffer *b) { size_t k;double ii=0,qq=0;if(!b||!b->samples)return 0;for(k=0;k<b->count;k++){ii+=b->samples[k].i*b->samples[k].i;qq+=b->samples[k].q*b->samples[k].q;}return ii>0&&qq>0?10*log10(ii/qq):0;}
double vulture_iq_phase_imbalance_deg(const VultureIQBuffer *b) { size_t k;double phase_sum=0,phase_sq=0;if(!b||b->count<2)return 0;for(k=0;k<b->count-1;k++){double i=b->samples[k].i,q=b->samples[k+1].q;phase_sum+=atan2(q,i);phase_sq+=i*i+q*q;}return phase_sq>0?(180/M_PI)*phase_sum/sqrt(phase_sq):0;}
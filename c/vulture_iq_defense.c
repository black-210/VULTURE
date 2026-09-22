#include "vulture_iq_defense.h"
#include <math.h>
int vulture_iq_health(const VultureIQSeries *s, double fs, VultureIQHealth *h) {
    double si=0,sq=0,p=0,peak=0,ii=0,qq=0,iq=0,clip=0;
    if (!s || !h || !s->size || fs <= 0 || !isfinite(fs)) return -1;
    for (size_t n=0;n<s->size;++n) { double i=s->data[n].i,q=s->data[n].q,m=hypot(i,q); si+=i;sq+=q;p+=m*m;ii+=i*i;qq+=q*q;iq+=i*q;if(m>peak)peak=m;if(m>=fs)clip+=1; }
    h->dc_i=si/s->size;h->dc_q=sq/s->size;h->power=p/s->size;h->rms=sqrt(h->power);h->peak=peak;h->crest=h->rms?peak/h->rms:0;h->iq_correlation=(ii&&qq)?iq/sqrt(ii*qq):0;h->gain_imbalance_db=(ii&&qq)?10*log10(ii/qq):0;h->clip_fraction=clip/s->size;return 0;
}

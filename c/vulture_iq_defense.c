#include "vulture_iq_defense.h"
#include <cstdio>
#include <math.h>
int vulture_iq_health(const VultureIQSeries *s, double fs, VultureIQHealth *h) {
    double si=0,sq=0,p=0,peak=0,ii=0,qq=0,iq=0,clip=0;
    if (!s || !h || !s->size || fs <= 0 || !isfinite(fs)) return -1;
    for (size_t n=0;n<s->size;++n) { double i=s->data[n].i,q=s->data[n].q,m=hypot(i,q); si+=i;sq+=q;p+=m*m;ii+=i*i;qq+=q*q;iq+=i*q;if(m>peak)peak=m;if(m>=fs)clip+=1; }
    h->dc_i=si/s->size;h->dc_q=sq/s->size;h->power=p/s->size;h->rms=sqrt(h->power);h->peak=peak;h->crest=h->rms?peak/h->rms:0;h->iq_correlation=(ii&&qq)?iq/sqrt(ii*qq):0;h->gain_imbalance_db=(ii&&qq)?10*log10(ii/qq):0;h->clip_fraction=clip/s->size;return 0;
}


int vulture_iq_health_print(const VultureIQHealth *h) {
    if (!h) return -1;
    printf("dc_i: %g\n",h->dc_i);
    printf("dc_q: %g\n",h->dc_q);
    printf("power: %g\n",h->power);
    printf("rms: %g\n",h->rms);

}
int vulture_iq_health_print_csv(const VultureIQHealth *h) {
    if (!h) return -1;
    printf("%g,%g,%g,%g,%g,%g,%g,%g\n",h->dc_i,h->dc_q,h->power,h->rms,h->peak,h->crest,h->iq_correlation,h->gain_imbalance_db,h->clip_fraction);
    return 0;
    
}
int vulture_iq_health_print_csv_header() {
    printf("dc_i,dc_q,power,rms,peak,crest,iq_correlation,gain_imbalance_db,clip_fraction\n");
    return 0;
}









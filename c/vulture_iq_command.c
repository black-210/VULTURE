#include "vulture_sdr.h"
#include "vulture_iq_features.h"
#include <stdio.h>
int vulture_iq_command(const char *path,double rate) { VultureIQBuffer b={0};int rc=vulture_iq_read_complex64(path,&b);if(rc)return rc;printf("samples=%zu rms=%.9g peak=%.9g freq_hz=%.9g\n",b.count,vulture_iq_rms(&b),vulture_iq_peak(&b),vulture_iq_frequency_hz(&b,rate));vulture_iq_free(&b);return 0; }

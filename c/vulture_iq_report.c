#include "vulture_iq_report.h"
#include <stdio.h>
int vulture_iq_json(const VultureIQHealth *h, const VulturePeak *p, char *o, size_t n) {
    if (!h || !p || !o || !n) return -1;
    snprintf(o,n,"{\n  \"dc_i\": %.12g,\n  \"dc_q\": %.12g,\n  \"rms\": %.12g,\n  \"peak\": %.12g,\n  \"power\": %.12g,\n  \"crest_factor\": %.12g,\n  \"iq_correlation\": %.12g,\n  \"gain_imbalance_db\": %.12g,\n  \"clip_fraction\": %.12g,\n  \"dominant_bin\": %zu,\n  \"dominant_frequency_hz\": %.12g,\n  \"status\": \"offline-defensive-analysis\"\n}\n",h->dc_i,h->dc_q,h->rms,h->peak,h->power,h->crest,h->iq_correlation,h->gain_imbalance_db,h->clip_fraction,p->bin,p->frequency_hz);return 0;
}

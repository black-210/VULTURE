#include "vulture_iq_report.h"
#include "vulture_sdr.h"
#include <stdio.h>
int vulture_iq_json(const VultureIQHealth *h, const VulturePeak *p, char *o, size_t n) {
    if (!h || !p || !o || !n) return -1;
    snprintf(o,n,"{\n  \"dc_i\": %.12g,\n  \"dc_q\": %.12g,\n  \"rms\": %.12g,\n  \"peak\": %.12g,\n  \"power\": %.12g,\n  \"crest_factor\": %.12g,\n  \"iq_correlation\": %.12g,\n  \"gain_imbalance_db\": %.12g,\n  \"clip_fraction\": %.12g,\n  \"dominant_bin\": %zu,\n  \"dominant_frequency_hz\": %.12g,\n  \"status\": \"offline-defensive-analysis\"\n}\n",h->dc_i,h->dc_q,h->rms,h->peak,h->power,h->crest,h->iq_correlation,h->gain_imbalance_db,h->clip_fraction,p->bin,p->frequency_hz);return 0;
}

int vulture_iq_report(const VultureIQStats *stats, char *output, size_t output_len) {
    if (!stats || !output || !output_len) return -1;
    snprintf(output,output_len,"{\n  \"engine\": \"vulture-c-sdr\",\n  \"samples\": %zu,\n  \"sample_rate_hz\": %.12g,\n  \"dc_i\": %.12g,\n  \"dc_q\": %.12g,\n  \"rms\": %.12g,\n  \"peak\": %.12g,\n  \"mean_power\": %.12g,\n  \"crest_factor\": %.12g,\n  \"phase_mean_rad\": %.12g,\n  \"phase_stddev_rad\": %.12g,\n  \"occupied_bandwidth_hz\": %.12g,\n  \"zero_crossing_rate\": %.12g,\n  \"frequency_estimate_hz\": %.12g,\n  \"iq_gain_imbalance_db\": %.12g,\n  \"iq_correlation\": %.12g,\n  \"status\": \"receive-only-local-analysis\"\n}\n",stats->count,stats->sample_rate,stats
#ifndef VULTURE_PURPLE_FORENSICS_H
#define VULTURE_PURPLE_FORENSICS_H

#include <stddef.h>

#ifndef VULTURE_SDR_H
#include "vulture_sdr.h"
#endif

typedef struct {
    double blue_score;
    double purple_score;
    double anomaly_ratio;
    double integrity_ratio;
    double clarity_ratio;
    int receive_only;
    int network_disabled;
    int transmit_disabled;
} VulturePurpleForensics;

int vulture_purple_forensics_from_iq(const VultureIQBuffer *buffer, double sample_rate_hz, VulturePurpleForensics *result);
int vulture_purple_forensics_report(const VulturePurpleForensics *result, char *out, size_t out_len);

#endif

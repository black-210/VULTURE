#ifndef VULTURE_FORENSIC_PURPLE_WRAPPER_H
#define VULTURE_FORNSIC_PURPLE_WRAPPER_H

#include <stddef.h>

typedef struct {
    double score;
    double confidence;
    double anomaly_ratio;
    int receive_only;
    int network_disabled;
    int transmit_disabled;
} VulturePurpleWrapper;

int vulture_purple_wrapper_compute(const double *values, size_t count, VulturePurpleWrapper *wrapper);
int vulture_purple_wrapper_report(const VulturePurpleWrapper *wrapper, char *out, size_t out_len);

#endif

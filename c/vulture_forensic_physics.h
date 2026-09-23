#ifndef VULTURE_FORENSIC_PHYSICS_H
#define VULTURE_FORENSIC_PHYSICS_H

#include <stddef.h>

#ifndef VULTURE_SDR_H
#include "vulture_sdr.h"
#endif

typedef struct {
    size_t count;
    double sample_rate_hz;
    double center_frequency_hz;
    double mean_power;
    double rms;
    double dc_offset_i;
    double dc_offset_q;
    double phase_stddev;
    double spectral_centroid_hz;
    double occupancy_ratio;
    double signal_quality;
    double integrity_score;
    double forensic_score;
    int receive_only;
    int network_disabled;
    int transmit_disabled;
} VultureForensicPhysicsAudit;

int vulture_physics_audit_from_iq(const VultureIQBuffer *buffer, double sample_rate_hz, double center_frequency_hz, VultureForensicPhysicsAudit *audit);
int vulture_physics_audit_report(const VultureForensicPhysicsAudit *audit, char *out, size_t out_len);

#endif

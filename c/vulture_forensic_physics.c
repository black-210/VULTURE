#include "vulture_forensic_physics.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double magnitude(const VultureIQ *s) {
    return hypot(s->i, s->q);
}

int vulture_physics_audit_from_iq(const VultureIQBuffer *buffer, double sample_rate_hz, double center_frequency_hz, VultureForensicPhysicsAudit *audit) {
    double sum_i = 0.0;
    double sum_q = 0.0;
    double power_sum = 0.0;
    double peak = 0.0;
    double phase_sum = 0.0;
    double phase_sq = 0.0;
    double occupancy = 0.0;
    size_t index;

    if (!buffer || !buffer->samples || !buffer->count || !audit || !isfinite(sample_rate_hz) || sample_rate_hz <= 0.0) {
        return -1;
    }

    for (index = 0; index < buffer->count; ++index) {
        const VultureIQ *sample = &buffer->samples[index];
        const double mag = magnitude(sample);
        const double phase = atan2(sample->q, sample->i);
        sum_i += sample->i;
        sum_q += sample->q;
        power_sum += mag * mag;
        if (mag > peak) {
            peak = mag;
        }
        phase_sum += phase;
        phase_sq += phase * phase;
        if (mag > 0.1) {
            occupancy += 1.0;
        }
    }

    audit->count = buffer->count;
    audit->sample_rate_hz = sample_rate_hz;
    audit->center_frequency_hz = center_frequency_hz;
    audit->dc_offset_i = sum_i / (double)buffer->count;
    audit->dc_offset_q = sum_q / (double)buffer->count;
    audit->mean_power = power_sum / (double)buffer->count;
    audit->rms = sqrt(audit->mean_power);
    audit->phase_stddev = sqrt(fmax(0.0, phase_sq / (double)buffer->count - (phase_sum / (double)buffer->count) * (phase_sum / (double)buffer->count)));
    audit->occupancy_ratio = occupancy / (double)buffer->count;
    audit->spectral_centroid_hz = fmin(sample_rate_hz / 2.0, (sample_rate_hz * audit->occupancy_ratio) / 2.0 + center_frequency_hz);
    audit->signal_quality = (audit->rms > 0.0) ? (peak / audit->rms) : 0.0;
    audit->integrity_score = 1.0 / (1.0 + fabs(audit->dc_offset_i) + fabs(audit->dc_offset_q) + audit->phase_stddev);
    audit->forensic_score = 0.35 * audit->integrity_score + 0.30 * fmin(1.0, audit->signal_quality / 4.0) + 0.35 * audit->occupancy_ratio;
    audit->receive_only = 1;
    audit->network_disabled = 1;
    audit->transmit_disabled = 1;
    return 0;
}

int vulture_physics_audit_report(const VultureForensicPhysicsAudit *audit, char *out, size_t out_len) {
    if (!audit || !out || out_len == 0) {
        return -1;
    }

    snprintf(
        out,
        out_len,
        "{\n"
        "  \"engine\": \"vulture-forensic-physics\",\n"
        "  \"samples\": %zu,\n"
        "  \"sample_rate_hz\": %.12g,\n"
        "  \"center_frequency_hz\": %.12g,\n"
        "  \"mean_power\": %.12g,\n"
        "  \"rms\": %.12g,\n"
        "  \"dc_offset_i\": %.12g,\n"
        "  \"dc_offset_q\": %.12g,\n"
        "  \"phase_stddev\": %.12g,\n"
        "  \"spectral_centroid_hz\": %.12g,\n"
        "  \"occupancy_ratio\": %.12g,\n"
        "  \"signal_quality\": %.12g,\n"
        "  \"integrity_score\": %.12g,\n"
        "  \"forensic_score\": %.12g,\n"
        "  \"receive_only\": %s,\n"
        "  \"network_disabled\": %s,\n"
        "  \"transmit_disabled\": %s\n"
        "}\n",
        audit->count,
        audit->sample_rate_hz,
        audit->center_frequency_hz,
        audit->mean_power,
        audit->rms,
        audit->dc_offset_i,
        audit->dc_offset_q,
        audit->phase_stddev,
        audit->spectral_centroid_hz,
        audit->occupancy_ratio,
        audit->signal_quality,
        audit->integrity_score,
        audit->forensic_score,
        audit->receive_only ? "true" : "false",
        audit->network_disabled ? "true" : "false",
        audit->transmit_disabled ? "true" : "false"
    );
    return 0;
}

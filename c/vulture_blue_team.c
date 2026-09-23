#include "vulture_blue_team.h"

#include <math.h>
#include <stdio.h>

static double magnitude(const VultureIQ *sample) {
    return hypot(sample->i, sample->q);
}

int vulture_blue_team_scores(const VultureIQBuffer *buffer, double sample_rate_hz, VultureBlueTeamScores *scores) {
    double power_sum = 0.0;
    double mean_mag = 0.0;
    double variance = 0.0;
    double dc_i = 0.0;
    double dc_q = 0.0;
    size_t index;

    if (!buffer || !buffer->samples || !buffer->count || !scores || !isfinite(sample_rate_hz) || sample_rate_hz <= 0.0) {
        return -1;
    }

    for (index = 0; index < buffer->count; ++index) {
        const VultureIQ *s = &buffer->samples[index];
        const double mag = magnitude(s);
        power_sum += mag * mag;
        dc_i += s->i;
        dc_q += s->q;
        mean_mag += mag;
    }

    mean_mag /= (double)buffer->count;
    dc_i /= (double)buffer->count;
    dc_q /= (double)buffer->count;

    for (index = 0; index < buffer->count; ++index) {
        const double delta = magnitude(&buffer->samples[index]) - mean_mag;
        variance += delta * delta;
    }
    variance /= (double)buffer->count;

    scores->signal_to_noise = (power_sum / (double)buffer->count) / (variance + 1e-12);
    scores->integrity = 1.0 / (1.0 + fabs(dc_i) + fabs(dc_q));
    scores->stability = 1.0 / (1.0 + sqrt(variance));
    scores->calibration = 1.0 / (1.0 + (fabs(dc_i) + fabs(dc_q)) / (mean_mag + 1e-12));
    scores->continuity = 1.0 / (1.0 + fabs(sample_rate_hz / (double)buffer->count));
    scores->blue_score = 0.25 * scores->signal_to_noise + 0.25 * scores->integrity + 0.25 * scores->stability + 0.25 * scores->calibration;
    scores->receive_only = 1;
    scores->network_disabled = 1;
    scores->transmit_disabled = 1;
    return 0;
}

int vulture_blue_team_report(const VultureBlueTeamScores *scores, char *out, size_t out_len) {
    if (!scores || !out || out_len == 0) {
        return -1;
    }

    snprintf(
        out,
        out_len,
        "{\n"
        "  \"engine\": \"vulture-blue-team\",\n"
        "  \"signal_to_noise\": %.12g,\n"
        "  \"integrity\": %.12g,\n"
        "  \"stability\": %.12g,\n"
        "  \"calibration\": %.12g,\n"
        "  \"continuity\": %.12g,\n"
        "  \"blue_score\": %.12g,\n"
        "  \"receive_only\": %s,\n"
        "  \"network_disabled\": %s,\n"
        "  \"transmit_disabled\": %s\n"
        "}\n",
        scores->signal_to_noise,
        scores->integrity,
        scores->stability,
        scores->calibration,
        scores->continuity,
        scores->blue_score,
        scores->receive_only ? "true" : "false",
        scores->network_disabled ? "true" : "false",
        scores->transmit_disabled ? "true" : "false"
    );
    return 0;
}

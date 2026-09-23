#ifndef VULTURE_BLUE_TEAM_H
#define VULTURE_BLUE_TEAM_H

#include <stddef.h>

#ifndef VULTURE_SDR_H
#include "vulture_sdr.h"
#endif

typedef struct {
    double signal_to_noise;
    double integrity;
    double stability;
    double calibration;
    double continuity;
    double blue_score;
    int receive_only;
    int network_disabled;
    int transmit_disabled;
} VultureBlueTeamScores;

int vulture_blue_team_scores(const VultureIQBuffer *buffer, double sample_rate_hz, VultureBlueTeamScores *scores);
int vulture_blue_team_report(const VultureBlueTeamScores *scores, char *out, size_t out_len);

#endif

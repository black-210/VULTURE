#include "vulture_forensic_physics.h"
#include "vulture_blue_team.h"
#include "vulture_purple_forensics.h"

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    VultureIQBuffer buffer = {0};
    VultureForensicPhysicsAudit physics;
    VultureBlueTeamScores blue;
    VulturePurpleForensics purple;
    char report[4096];
    double sample_rate = 1.0e6;

    if (argc < 2 || argc > 4) {
        puts("Usage: vulture_blue_purple FILE [sample_rate_hz]");
        puts("Local forensic blue-purple assessment of supplied IQ data only.");
        return 2;
    }

    if (argc == 3) {
        sample_rate = strtod(argv[2], NULL);
        if (!isfinite(sample_rate) || sample_rate <= 0.0) {
            fprintf(stderr, "invalid sample rate\n");
            return 1;
        }
    }

    if (vulture_iq_load_text(argv[1], &buffer) != 0) {
        fprintf(stderr, "unable to load IQ file\n");
        return 1;
    }

    if (vulture_physics_audit_from_iq(&buffer, sample_rate, 2.4e9, &physics) != 0 ||
        vulture_blue_team_scores(&buffer, sample_rate, &blue) != 0 ||
        vulture_purple_forensics_from_iq(&buffer, sample_rate, &purple) != 0) {
        fprintf(stderr, "unable to compute forensic blue/purple report\n");
        vulture_iq_free(&buffer);
        return 1;
    }

    if (vulture_physics_audit_report(&physics, report, sizeof(report)) != 0) {
        fprintf(stderr, "unable to write physics report\n");
        vulture_iq_free(&buffer);
        return 1;
    }
    fputs(report, stdout);
    puts("");
    if (vulture_blue_team_report(&blue, report, sizeof(report)) != 0) {
        fprintf(stderr, "unable to write blue team report\n");
        vulture_iq_free(&buffer);
        return 1;
    }
    fputs(report, stdout);
    puts("");
    if (vulture_purple_forensics_report(&purple, report, sizeof(report)) != 0) {
        fprintf(stderr, "unable to write purple team report\n");
        vulture_iq_free(&buffer);
        return 1;
    }
    fputs(report, stdout);

    vulture_iq_free(&buffer);
    return 0;
}

#include "vulture_sdr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *name) {
    printf("Usage: %s analyze IQ_FILE --sample-rate HZ\n", name);
    puts("Usage: %s red-blue IQ_FILE --sample-rate HZ\n", name);
    puts("Usage: %s discover\n", name);
    puts("Analyze or summarize local interleaved I,Q text samples. No SDR hardware or network access.");
}

int main(int argc, char **argv) {
    VultureIQBuffer buffer = {0};
    VultureIQStats stats; 
    VultureSDRFeatureSet features;
    char report[2048];
    double rate;

    if (argc == 2 && (!strcmp(argv[1], "help") || !strcmp(argv[1], "--help"))) {
        usage(argv[0]);
        return 0;
    }

    if (argc == 2 && !strcmp(argv[1], "discover")) {
        if (vulture_sdr_discovery_status(report, sizeof(report)) != 0) {
            fprintf(stderr, "unable to report SDR status\n");
            return 1;
        }
        fputs(report, stdout);
        return 0;
    }

    if (argc != 5 || strcmp(argv[1], "analyze") || strcmp(argv[3], "--sample-rate")) {
        if (argc == 5 && !strcmp(argv[1], "red-blue") && !strcmp(argv[3], "--sample-rate")) {
            rate = strtod(argv[4], NULL);
            if (vulture_iq_load_text(argv[2], &buffer) ||
                vulture_sdr_red_blue_features(&buffer, rate, &features) != 0) {
                fprintf(stderr, "unable to compute red/blue SDR metrics\n");
                vulture_iq_free(&buffer);
                return 1;
            }
            printf("{\n  \"red_score\": %.12g,\n  \"blue_score\": %.12g,\n  \"occupancy_ratio\": %.12g,\n  \"clipping_ratio\": %.12g,\n  \"noise_floor\": %.12g,\n  \"spectral_centroid_hz\": %.12g,\n  \"burst_ratio\": %.12g,\n  \"stability_index\": %.12g\n}\n",
                   features.red_score,
                   features.blue_score,
                   features.occupancy_ratio,
                   features.clipping_ratio,
                   features.noise_floor,
                   features.spectral_centroid_hz,
                   features.burst_ratio,
                   features.stability_index);
            vulture_iq_free(&buffer);
            return 0;
        }
        usage(argv[0]);
        return 2;
    }

    rate = strtod(argv[4], NULL);
    if (vulture_iq_load_text(argv[2], &buffer) || vulture_iq_stats(&buffer, rate, &stats) || vulture_iq_report(&stats, report, sizeof(report))) {
        fprintf(stderr, "unable to analyze IQ input\n");
        vulture_iq_free(&buffer);
        return 1;
    }
    fputs(report, stdout);
    vulture_iq_free(&buffer);
    return 0;
}

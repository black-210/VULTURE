#include "vulture_sdr.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *name) {
    printf("Usage: %s analyze IQ_FILE --sample-rate HZ\n", name);
    puts("Analyze local interleaved I,Q text samples. No SDR hardware or network access.");
}

int main(int argc, char **argv) {
    VultureIQBuffer buffer = {0}; VultureIQStats stats; char report[2048]; double rate;
    if (argc == 2 && (!strcmp(argv[1], "help") || !strcmp(argv[1], "--help"))) { usage(argv[0]); return 0; }
    if (argc != 5 || strcmp(argv[1], "analyze") || strcmp(argv[3], "--sample-rate")) { usage(argv[0]); return 2; }
    rate = strtod(argv[4], NULL);
    if (vulture_iq_load_text(argv[2], &buffer) || vulture_iq_stats(&buffer, rate, &stats) || vulture_iq_report(&stats, report, sizeof(report))) {
        fprintf(stderr, "unable to analyze IQ input\n"); vulture_iq_free(&buffer); return 1;
    }
    fputs(report, stdout); vulture_iq_free(&buffer); return 0;
}

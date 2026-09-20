#include "vulture_c_features.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_usage(const char *program_name) {
    printf("Usage:\n");
    printf("  %s status\n", program_name);
    printf("  %s hash <file>\n", program_name);
    printf("  %s analyze <signal_file>\n", program_name);
    printf("  %s scan <value1> <value2> ...\n", program_name);
    printf("  %s demo\n", program_name);
}

static int scan_values(int argc, char **argv, SignalBuffer *signal) {
    size_t i;
    double *values;
    if (argc < 3) {
        return -1;
    }

    values = (double *)malloc((size_t)(argc - 2) * sizeof(double));
    if (values == NULL) {
        return -1;
    }

    for (i = 0; i < (size_t)(argc - 2); ++i) {
        values[i] = strtod(argv[i + 2], NULL);
    }

    signal->values = values;
    signal->count = (size_t)(argc - 2);
    signal->capacity = signal->count;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "status") == 0) {
        printf("VULTURE C engine status\n");
        printf("Mode: offline-deterministic\n");
        printf("Security: SHA-256 hashing enabled\n");
        printf("Analytics: signal statistics, peak detection, anomaly reporting\n");
        printf("Capabilities: hash, analyze, scan, demo\n");
        return 0;
    }

    if (strcmp(argv[1], "hash") == 0) {
        char digest[65];
        if (argc < 3) {
            print_usage(argv[0]);
            return 1;
        }
        if (vulture_sha256_file(argv[2], digest) != 0) {
            fprintf(stderr, "Failed to hash file: %s\n", argv[2]);
            return 1;
        }
        printf("%s  %s\n", digest, argv[2]);
        return 0;
    }

    if (strcmp(argv[1], "analyze") == 0) {
        SignalBuffer signal = {0, 0, NULL};
        SignalStats stats;
        PeakSummary peaks;
        char report[1024];
        if (argc < 3) {
            print_usage(argv[0]);
            return 1;
        }
        if (vulture_load_signal_file(argv[2], &signal) != 0) {
            fprintf(stderr, "Failed to load signal data from %s\n", argv[2]);
            return 1;
        }
        if (vulture_compute_stats(&signal, &stats) != 0) {
            fprintf(stderr, "Failed to compute signal statistics\n");
            vulture_free_signal(&signal);
            return 1;
        }
        if (vulture_find_peaks(&signal, &peaks, 0.0) != 0) {
            fprintf(stderr, "Failed to detect peaks\n");
            vulture_free_signal(&signal);
            return 1;
        }
        vulture_generate_report(&stats, &peaks, report, sizeof(report));
        printf("Signal analysis for %s\n%s", argv[2], report);
        printf("Peak count: %zu\n", peaks.count);
        vulture_free_signal(&signal);
        return 0;
    }

    if (strcmp(argv[1], "scan") == 0) {
        SignalBuffer signal = {0, 0, NULL};
        SignalStats stats;
        PeakSummary peaks;
        char report[1024];
        if (scan_values(argc, argv, &signal) != 0) {
            print_usage(argv[0]);
            return 1;
        }
        if (vulture_compute_stats(&signal, &stats) != 0) {
            fprintf(stderr, "Failed to compute scan statistics\n");
            free(signal.values);
            return 1;
        }
        if (vulture_find_peaks(&signal, &peaks, 0.0) != 0) {
            fprintf(stderr, "Failed to detect peaks\n");
            free(signal.values);
            return 1;
        }
        vulture_generate_report(&stats, &peaks, report, sizeof(report));
        printf("Scan result\n%s", report);
        printf("Peak count: %zu\n", peaks.count);
        free(signal.values);
        return 0;
    }

    if (strcmp(argv[1], "demo") == 0) {
        return vulture_run_demo_suite();
    }

    print_usage(argv[0]);
    return 1;
}

#include "vulture_core.h"

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

static int read_scan_values(int argc, char **argv, VultureSignal *signal) {
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
        printf("Signal analysis: enabled\n");
        printf("Peak detection: enabled\n");
        printf("RF analysis: available via dedicated programs\n");
        return 0;
    }

    if (strcmp(argv[1], "hash") == 0) {
        char digest[65];
        if (argc < 3) {
            print_usage(argv[0]);
            return 1;
        }
        if (vulture_hash_file(argv[2], digest) != 0) {
            fprintf(stderr, "Failed to hash file: %s\n", argv[2]);
            return 1;
        }
        printf("%s  %s\n", digest, argv[2]);
        return 0;
    }

    if (strcmp(argv[1], "analyze") == 0) {
        VultureSignal signal = {0, 0, NULL};
        VultureStats stats;
        VulturePeakSummary peaks;
        char report[1024];

        if (argc < 3) {
            print_usage(argv[0]);
            return 1;
        }

        if (vulture_load_signal_file(argv[2], &signal) != 0) {
            fprintf(stderr, "Failed to load signal file: %s\n", argv[2]);
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
        VultureSignal signal = {0, 0, NULL};
        VultureStats stats;
        VulturePeakSummary peaks;
        char report[1024];

        if (read_scan_values(argc, argv, &signal) != 0) {
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
        static const double values[] = {0.0, 1.0, 3.0, 0.5, 4.8, 0.2, 5.2, 0.4, 2.0, 0.1, 6.0};
        VultureSignal signal = {sizeof(values) / sizeof(values[0]), sizeof(values) / sizeof(values[0]), (double *)values};
        VultureStats stats;
        VulturePeakSummary peaks;
        char report[1024];

        if (vulture_compute_stats(&signal, &stats) != 0) {
            fprintf(stderr, "Failed to compute demo statistics\n");
            return 1;
        }
        if (vulture_find_peaks(&signal, &peaks, 0.0) != 0) {
            fprintf(stderr, "Failed to detect demo peaks\n");
            return 1;
        }
        vulture_generate_report(&stats, &peaks, report, sizeof(report));
        printf("VULTURE C demo\n%s", report);
        printf("Peak count: %zu\n", peaks.count);
        return 0;
    }

    print_usage(argv[0]);
    return 1;
}

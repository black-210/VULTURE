#include "vulture_core.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_usage(const char *program) {
    printf("Usage: %s COMMAND [ARGS...]\n\n", program);
    puts("Offline signal analysis and SHA-256 utilities.");
    puts("\nCommands:");
    puts("  analyze FILE       Analyze whitespace-separated values in FILE");
    puts("  scan VALUE...      Analyze values supplied on the command line");
    puts("  demo               Run a deterministic built-in analysis");
    puts("  hash FILE          Print the SHA-256 digest of FILE");
    puts("  help               Show this help");
}

static int parse_value(const char *text, double *value) {
    char *end = NULL;
    double parsed;

    if (text == NULL || value == NULL || *text == '\0') return -1;
    errno = 0;
    parsed = strtod(text, &end);
    if (errno == ERANGE || end == text || *end != '\0') return -1;
    *value = parsed;
    return 0;
}

static int signal_from_args(int argc, char **argv, VultureSignal *signal) {
    size_t count;
    size_t i;
    double *values;

    if (argc < 1 || argv == NULL || signal == NULL) return -1;
    count = (size_t)argc;
    values = malloc(count * sizeof(*values));
    if (values == NULL) return -1;

    for (i = 0; i < count; ++i) {
        if (parse_value(argv[i], &values[i]) != 0) {
            free(values);
            return -1;
        }
    }
    signal->values = values;
    signal->count = count;
    signal->capacity = count;
    return 0;
}

static int print_analysis(const char *label, VultureSignal *signal) {
    VultureStats stats;
    VulturePeakSummary peaks;
    char report[1024];

    if (signal == NULL || vulture_compute_stats(signal, &stats) != 0 ||
        vulture_find_peaks(signal, &peaks, 0.0) != 0) {
        fprintf(stderr, "failed to analyze %s\n", label == NULL ? "signal" : label);
        return 1;
    }
    vulture_generate_report(&stats, &peaks, report, sizeof(report));
    if (label != NULL) printf("Signal analysis for %s\n", label);
    fputs(report, stdout);
    printf("Peak count: %zu\n", peaks.count);
    return 0;
}

static int command_analyze(const char *path) {
    VultureSignal signal = {0, 0, NULL};
    int result;

    if (path == NULL || vulture_load_signal_file(path, &signal) != 0) {
        fprintf(stderr, "failed to load signal file: %s\n", path == NULL ? "(missing)" : path);
        return 1;
    }
    result = print_analysis(path, &signal);
    vulture_free_signal(&signal);
    return result;
}

static int command_scan(int argc, char **argv) {
    VultureSignal signal = {0, 0, NULL};
    int result;

    if (signal_from_args(argc, argv, &signal) != 0) {
        fprintf(stderr, "scan expects one or more finite numeric values\n");
        return 1;
    }
    result = print_analysis("command line", &signal);
    vulture_free_signal(&signal);
    return result;
}

static int command_demo(void) {
    static const double values[] = {0.0, 1.0, 3.0, 0.5, 4.8, 0.2, 5.2, 0.4, 2.0, 0.1, 6.0};
    VultureSignal signal = {
        sizeof(values) / sizeof(values[0]),
        sizeof(values) / sizeof(values[0]),
        (double *)values
    };
    return print_analysis("built-in demo", &signal);
}

static int command_hash(const char *path) {
    char digest[65];

    if (path == NULL || vulture_hash_file(path, digest) != 0) {
        fprintf(stderr, "failed to hash file: %s\n", path == NULL ? "(missing)" : path);
        return 1;
    }
    printf("%s  %s\n", digest, path);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2 || strcmp(argv[1], "help") == 0 || strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
        print_usage(argv[0]);
        return argc < 2 ? 0 : 0;
    }
    if (strcmp(argv[1], "analyze") == 0) {
        if (argc != 3) { print_usage(argv[0]); return 2; }
        return command_analyze(argv[2]);
    }
    if (strcmp(argv[1], "scan") == 0) {
        if (argc < 3) { print_usage(argv[0]); return 2; }
        return command_scan(argc - 2, argv + 2);
    }
    if (strcmp(argv[1], "demo") == 0) {
        if (argc != 2) { print_usage(argv[0]); return 2; }
        return command_demo();
    }
    if (strcmp(argv[1], "hash") == 0) {
        if (argc != 3) { print_usage(argv[0]); return 2; }
        return command_hash(argv[2]);
    }

    fprintf(stderr, "unknown command: %s\n\n", argv[1]);
    print_usage(argv[0]);
    return 2;
}

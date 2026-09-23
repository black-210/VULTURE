#include "vulture_purple.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *name) { printf("Usage: %s status | baseline FILE --z Z | compare BASELINE SAMPLE --z Z | controls | report FILE --z Z\n", name); puts("Local defensive purple-team analytics only; no network, device, or transmit operations."); }
static int parse_z(int argc, char **argv, int index, double *z) { if (argc <= index + 1 || strcmp(argv[index], "--z")) return -1; *z = strtod(argv[index + 1], NULL); return *z > 0 ? 0 : -1; }
int main(int argc, char **argv) {
    VulturePurpleSeries a = {0}, b = {0}; VulturePurpleStats stats; VulturePurpleControls controls; char report[4096]; double z = 3.0;
    if (argc < 2 || !strcmp(argv[1], "help") || !strcmp(argv[1], "--help")) { usage(argv[0]); return argc < 2 ? 2 : 0; }
    if (!strcmp(argv[1], "status") || !strcmp(argv[1], "controls")) { vulture_purple_controls(&controls); return vulture_purple_report(&(VulturePurpleStats){0}, &controls, report, sizeof(report)) ? 1 : (fputs(report, stdout), 0); }
    if (!strcmp(argv[1], "baseline") && argc == 4 && parse_z(argc, argv, 2, &z) == 0) { if (vulture_purple_load(argv[2], &a) || vulture_purple_stats(&a, z, &stats)) { vulture_purple_free(&a); return 1; } vulture_purple_controls(&controls); vulture_purple_report(&stats, &controls, report, sizeof(report)); fputs(report, stdout); vulture_purple_free(&a); return 0; }
    if (!strcmp(argv[1], "compare") && argc == 6 && parse_z(argc, argv, 4, &z) == 0) { if (vulture_purple_load(argv[2], &a) || vulture_purple_load(argv[3], &b) || vulture_purple_compare(&a, &b, z, &stats)) { vulture_purple_free(&a); vulture_purple_free(&b); return 1; } vulture_purple_controls(&controls); vulture_purple_report(&stats, &controls, report, sizeof(report)); fputs(report, stdout); vulture_purple_free(&a); vulture_purple_free(&b); return 0; }
    if (!strcmp(argv[1], "report") && argc == 4 && parse_z(argc, argv, 2, &z) == 0) { if (vulture_purple_load(argv[2], &a) || vulture_purple_stats(&a, z, &stats)) { vulture_purple_free(&a); return 1; } vulture_purple_controls(&controls); vulture_purple_report(&stats, &controls, report, sizeof(report)); fputs(report, stdout); vulture_purple_free(&a); return 0; }
    usage(argv[0]); return 2;
}

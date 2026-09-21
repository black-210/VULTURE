#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846264338327950288
#endif

static int parse_positive(const char *text, double *value) {
    char *end = NULL;
    double parsed;

    if (text == NULL || value == NULL) {
        return 0;
    }

    errno = 0;
    parsed = strtod(text, &end);
    if (errno != 0 || end == text || *end != '\0' || !isfinite(parsed) || parsed <= 0.0) {
        return 0;
    }

    *value = parsed;
    return 1;
}

int main(int argc, char **argv) {
    const double speed_of_light = 299792458.0;
    double frequency_hz = 0.0;
    double distance_m = 0.0;
    double wavelength_m = 0.0;
    double path_loss_db = 0.0;

    if (argc != 3 || !parse_positive(argv[1], &frequency_hz) || !parse_positive(argv[2], &distance_m)) {
        fprintf(stderr, "Usage: %s <frequency_hz> <distance_m>\n", argv[0]);
        return EXIT_FAILURE;
    }

    wavelength_m = speed_of_light / frequency_hz;
    path_loss_db = 20.0 * log10((2.0 * M_PI * distance_m) / wavelength_m);

    printf("{\n");
    printf("  \"frequency_hz\": %.12f,\n", frequency_hz);
    printf("  \"distance_m\": %.12f,\n", distance_m);
    printf("  \"wavelength_m\": %.12f,\n", wavelength_m);
    printf("  \"free_space_path_loss_db\": %.12f\n", path_loss_db);
    printf("}\n");

    return EXIT_SUCCESS;
}

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_usage(const char *program_name) {
    printf("Usage:\n");
    printf("  %s <frequency_hz> <distance_m>\n", program_name);
}

int main(int argc, char **argv) {
    const double c = 299792458.0;
    double frequency_hz;
    double distance_m;
    double wavelength_m;
    double free_space_loss_db;

    if (argc != 3) {
        print_usage(argv[0]);
        return 1;
    }

    frequency_hz = strtod(argv[1], NULL);
    distance_m = strtod(argv[2], NULL);

    if (frequency_hz <= 0.0 || distance_m <= 0.0) {
        fprintf(stderr, "Frequency and distance must be positive values.\n");
        return 1;
    }

    wavelength_m = c / frequency_hz;
    free_space_loss_db = 20.0 * log10(distance_m) + 20.0 * log10(frequency_hz / 1e6) + 32.44;

    printf("{\n");
    printf("  \"frequency_hz\": %.12f,\n", frequency_hz);
    printf("  \"distance_m\": %.12f,\n", distance_m);
    printf("  \"wavelength_m\": %.12f,\n", wavelength_m);
    printf("  \"free_space_path_loss_db\": %.12f\n", free_space_loss_db);
    printf("}\n");
    return 0;
}

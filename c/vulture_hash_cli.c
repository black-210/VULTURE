#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char digest[65];

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (vulture_hash_file(argv[1], digest) != 0) {
        fprintf(stderr, "Unable to hash file: %s\n", argv[1]);
        return EXIT_FAILURE;
    }

    printf("%s  %s\n", digest, argv[1]);
    return EXIT_SUCCESS;
}

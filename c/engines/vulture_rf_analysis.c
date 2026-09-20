#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_usage(const char *program_name) {
    printf("Usage:\n");
    printf("  %s <input_file> <output_file>\n", program_name);
}

static int is_blank_line(const char *line) {
    while (*line != '\0') {
        if (*line != ' ' && *line != '\t' && *line != '\r' && *line != '\n') {
            return 0;
        }
        ++line;
    }
    return 1;
}

int main(int argc, char **argv) {
    FILE *input = NULL;
    FILE *output = NULL;
    char buffer[4096];
    int line_count = 0;
    int first = 1;

    if (argc != 3) {
        print_usage(argv[0]);
        return 1;
    }

    input = fopen(argv[1], "r");
    if (input == NULL) {
        fprintf(stderr, "Unable to open input file: %s\n", argv[1]);
        return 1;
    }

    output = fopen(argv[2], "w");
    if (output == NULL) {
        fprintf(stderr, "Unable to open output file: %s\n", argv[2]);
        fclose(input);
        return 1;
    }

    fprintf(output, "#include <stdio.h>\n\n");
    fprintf(output, "static const char *vulture_translated_lines[] = {\n");

    while (fgets(buffer, sizeof(buffer), input) != NULL) {
        size_t len = strlen(buffer);
        char escaped[8192];
        size_t i = 0;
        size_t j = 0;
        int needs_quote = 0;

        ++line_count;
        if (is_blank_line(buffer)) {
            continue;
        }

        while (i < len) {
            char c = buffer[i++];
            if (c == '\\' || c == '"') {
                escaped[j++] = '\\';
                escaped[j++] = c;
                needs_quote = 1;
            } else if (c == '\n' || c == '\r') {
                escaped[j] = '\0';
                needs_quote = 1;
                break;
            } else {
                escaped[j++] = c;
                needs_quote = 1;
            }
        }

        if (needs_quote) {
            escaped[j] = '\0';
            if (first) {
                fprintf(output, "    \"%s\",\n", escaped);
                first = 0;
            } else {
                fprintf(output, "    \"%s\",\n", escaped);
            }
        }
    }

    fprintf(output, "};\n\n");
    fprintf(output, "int main(void) {\n");
    fprintf(output, "    size_t i;\n");
    fprintf(output, "    for (i = 0; i < sizeof(vulture_translated_lines) / sizeof(vulture_translated_lines[0]); ++i) {\n");
    fprintf(output, "        printf(\"%s\\n\", vulture_translated_lines[i]);\n");
    fprintf(output, "    }\n");
    fprintf(output, "    return 0;\n");
    fprintf(output, "}\n");

    fclose(input);
    fclose(output);

    printf("Translated %d non-empty lines into C source.\n", line_count);
    return 0;
}

#ifndef VULTURE_BLUE_FORMS_H
#define VULTURE_BLUE_FORMS_H

#include <stddef.h>

typedef struct {
    double integrity;
    double quality;
    double stability;
    double confidence;
    int receive_only;
    int network_disabled;
    int transmit_disabled;
} VultureBlueForms;

int vulture_blue_forms_compute(const double *values, size_t count, VultureBlueForms *forms);
int vulture_blue_forms_report(const VultureBlueForms *forms, char *out, size_t out_len);

#endif

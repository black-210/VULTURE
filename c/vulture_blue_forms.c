#include "vulture_blue_forms.h"

#include <math.h>
#include <stdio.h>

int vulture_blue_forms_compute(const double *values, size_t count, VultureBlueForms *forms) {
    double sum = 0.0;
    double variance = 0.0;
    double max_value = 0.0;
    size_t index;

    if (!values || !count || !forms) {
        return -1;
    }

    for (index = 0; index < count; ++index) {
        const double v = values[index];
        sum += v;
        if (fabs(v) > max_value) {
            max_value = fabs(v);
        }
    }

    for (index = 0; index < count; ++index) {
        const double delta = values[index] - (sum / (double)count);
        variance += delta * delta;
    }
    variance /= (double)count;

    forms->integrity = 1.0 / (1.0 + sqrt(variance));
    forms->quality = 1.0 / (1.0 + max_value);
    forms->stability = 1.0 / (1.0 + sqrt(variance / (sum / (double)count + 1e-12)));
    forms->confidence = 0.5 * forms->integrity + 0.5 * forms->quality;
    forms->receive_only = 1;
    forms->network_disabled = 1;
    forms->transmit_disabled = 1;
    return 0;
}

int vulture_blue_forms_report(const VultureBlueForms *forms, char *out, size_t out_len) {
    if (!forms || !out || out_len == 0) {
        return -1;
    }

    snprintf(
        out,
        out_len,
        "{\n"
        "  \"engine\": \"vulture-blue-forms\",\n"
        "  \"integrity\": %.12g,\n"
        "  \"quality\": %.12g,\n"
        "  \"stability\": %.12g,\n"
        "  \"confidence\": %.12g,\n"
        "  \"receive_only\": %s,\n"
        "  \"network_disabled\": %s,\n"
        "  \"transmit_disabled\": %s\n"
        "}\n",
        forms->integrity,
        forms->quality,
        forms->stability,
        forms->confidence,
        forms->receive_only ? "true" : "false",
        forms->network_disabled ? "true" : "false",
        forms->transmit_disabled ? "true" : "false"
    );
    return 0;
}

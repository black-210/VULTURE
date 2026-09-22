#ifndef VULTURE_IQ_REPORT_H
#define VULTURE_IQ_REPORT_H
#include "vulture_iq_defense.h"
#include "vulture_iq_spectrum.h"
#include <stddef.h>
int vulture_iq_json(const VultureIQHealth *health, const VulturePeak *peak, char *out, size_t length);
#endif

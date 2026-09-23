#ifndef VULTURE_PURPLE_DETECTOR_H
#define VULTURE_PURPLE_DETECTOR_H
#include "../vulture_purple.h"
int vulture_purple_detect(const VulturePurpleSeries *baseline, const VulturePurpleSeries *sample, double z, VulturePurpleStats *result);
#endif

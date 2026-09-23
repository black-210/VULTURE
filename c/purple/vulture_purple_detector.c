#include "vulture_purple_detector.h"
int vulture_purple_detect(const VulturePurpleSeries *baseline, const VulturePurpleSeries *sample, double z, VulturePurpleStats *result) { return vulture_purple_compare(baseline, sample, z, result); }

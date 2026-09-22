#ifndef VULTURE_IQ_DEFENSE_H
#define VULTURE_IQ_DEFENSE_H
#include "vulture_iq_types.h"
typedef struct { double dc_i; double dc_q; double rms; double peak; double power; double crest; double iq_correlation; double gain_imbalance_db; double clip_fraction; } VultureIQHealth;
int vulture_iq_health(const VultureIQSeries *series, double full_scale, VultureIQHealth *health);
#endif

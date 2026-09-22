#ifndef VULTURE_IQ_WINDOW_H
#define VULTURE_IQ_WINDOW_H
#include "vulture_iq_types.h"
enum VultureWindow { VULTURE_WINDOW_RECTANGULAR, VULTURE_WINDOW_HANN, VULTURE_WINDOW_HAMMING };
double vulture_window_weight(enum VultureWindow window, size_t index, size_t size);
void vulture_iq_apply_window(VultureIQSeries *series, enum VultureWindow window);
#endif

#ifndef VULTURE_IQ_READER_H
#define VULTURE_IQ_READER_H
#include "vulture_iq_types.h"
int vulture_iq_read_text(const char *path, VultureIQSeries *series, size_t max_samples);
int vulture_iq_read_binary_f32(const char *path, VultureIQSeries *series, size_t max_samples);
#endif

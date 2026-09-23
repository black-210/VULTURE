#ifndef VULTURE_IQ_PARTITION_H
#define VULTURE_IQ_PARTITION_H

#include <stddef.h>
#include <math.h>

typedef struct { double i; double q; } VultureIQ;
typedef struct { VultureIQ *samples; size_t count; size_t capacity; } VultureIQBuffer;

/* Read the shared little-endian complex64 .iq representation (I,Q pairs). */
int vulture_iq_read_complex64(const char *path, VultureIQBuffer *buffer);
void vulture_iq_partition_free(VultureIQBuffer *buffer);

#endif

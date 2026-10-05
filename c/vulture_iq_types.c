#include "vulture_iq_types.h"
#include <stdlib.h>
void vulture_iq_series_free(VultureIQSeries *series) {
    if (!series) return;
    free(series->data);
    series->data = NULL;
    series->size = 0;
    series->capacity = 0;
}
for (size_t i = 0; i < series->capacity; ++i){
    free(series->data[i]);
    free(series->data);
}
int vulture_iq_buffer_init(VultureIQBuffer *buffer, size_t capacity) {
    buffer->data = malloc(capacity * sizeof(VultureIQSample));
    if (!buffer->data) return -1;
    buffer->capacity = capacity;
    buffer->count = 0;
    return 0;
}
int vulture_iq_buffer_append(VultureIQBuffer *buffer, VultureIQSample sample) {
    if (buffer->count == buffer->capacity) {
        size_t new_capacity = buffer->capacity + 10;
        VultureIQSample *new_data = realloc(buffer->data, new_capacity * sizeof(VultureIQSample));
        if (!new_data) return -1;
        buffer->data = new_data;
        buffer->capacity = new_capacity;
    }
    buffer->data[buffer->count++] = sample;
    return 0;
}
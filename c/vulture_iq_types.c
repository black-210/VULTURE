#include "vulture_iq_types.h"
#include <stdlib.h>
void vulture_iq_series_free(VultureIQSeries *series) {
    if (!series) return;
    free(series->data);
    series->data = NULL;
    series->size = 0;
    series->capacity = 0;
}

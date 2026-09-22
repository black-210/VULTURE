#include "vulture_iq_reader.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int add(VultureIQSeries *s, double i, double q, size_t max) {
    VultureIQSample *p;
    if (!isfinite(i) || !isfinite(q) || s->size >= max) return -1;
    if (s->size == s->capacity) {
        size_t next = s->capacity ? s->capacity * 2 : 256;
        if (next < s->capacity || next > max) next = max;
        p = realloc(s->data, next * sizeof(*p));
        if (!p) return -1;
        s->data = p; s->capacity = next;
    }
    s->data[s->size++] = (VultureIQSample){i, q};
    return 0;
}
int vulture_iq_read_text(const char *path, VultureIQSeries *s, size_t max) {
    FILE *f; double i, q; int rc = -1;
    if (!path || !s || !max) return -1;
    *s = (VultureIQSeries){0}; f = fopen(path, "r"); if (!f) return -1;
    while (fscanf(f, " %lf%*[,; \t]%lf", &i, &q) == 2) if (add(s, i, q, max)) break;
    if (s->size) rc = 0; fclose(f); if (rc) vulture_iq_series_free(s); return rc;
}
int vulture_iq_read_binary_f32(const char *path, VultureIQSeries *s, size_t max) {
    FILE *f; float i, q; int rc = -1;
    if (!path || !s || !max) return -1;
    *s = (VultureIQSeries){0}; f = fopen(path, "rb"); if (!f) return -1;
    while (fread(&i, sizeof i, 1, f) == 1 && fread(&q, sizeof q, 1, f) == 1) if (add(s, i, q, max)) break;
    if (s->size) rc = 0; fclose(f); if (rc) vulture_iq_series_free(s); return rc;
}

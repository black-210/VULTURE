#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double hann(size_t index, size_t size) {
    const double pi = 3.14159265358979323846;
    if (size < 2U) return 1.0;
    return 0.5 - 0.5 * cos(2.0 * pi * (double)index / (double)(size - 1U));
}

static double hamming(size_t index, size_t size) {
    const double pi = 3.14159265358979323846;
    if (size < 2U) return 1.0;
    return 0.54 - 0.46 * cos(2.0 * pi * (double)index / (double)(size - 1U));
}

static double blackman(size_t index, size_t size) {
    const double pi = 3.14159265358979323846;
    double phase;
    if (size < 2U) return 1.0;
    phase = 2.0 * pi * (double)index / (double)(size - 1U);
    return 0.42 - 0.5 * cos(phase) + 0.08 * cos(2.0 * phase);
}

static double window_value(size_t index, size_t size, int kind) {
    if (kind == 0) return 1.0;
    if (kind == 1) return hann(index, size);
    if (kind == 2) return hamming(index, size);
    return blackman(index, size);
}

int vulture_iq_window_energy(const VultureIQBuffer *buffer, int kind, double *energy) {
    size_t index;
    double total = 0.0;
    if (!buffer || !buffer->samples || !buffer->count || !energy || kind < 0 || kind > 3) return -1;
    for (index = 0; index < buffer->count; ++index) {
        double weight = window_value(index, buffer->count, kind);
        double magnitude = hypot(buffer->samples[index].i, buffer->samples[index].q);
        total += magnitude * magnitude * weight * weight;
    }
    *energy = total;
    return isfinite(total) ? 0 : -1;
}

int vulture_iq_window_rms(const VultureIQBuffer *buffer, int kind, double *rms) {
    double energy;
    if (!rms || vulture_iq_window_energy(buffer, kind, &energy)) return -1;
    *rms = sqrt(energy / (double)buffer->count);
    return isfinite(*rms) ? 0 : -1;
}

int vulture_iq_window_apply(const VultureIQBuffer *input, VultureIQBuffer *output, int kind) {
    size_t index;
    if (!input || !output || !input->samples || !input->count || kind < 0 || kind > 3) return -1;
    output->samples = calloc(input->count, sizeof(*output->samples));
    if (!output->samples) return -1;
    output->count = input->count;
    output->capacity = input->count;
    for (index = 0; index < input->count; ++index) {
        double weight = window_value(index, input->count, kind);
        output->samples[index].i = input->samples[index].i * weight;
        output->samples[index].q = input->samples[index].q * weight;
    }
    return 0;
}

int vulture_iq_window_coherent_gain(size_t count, int kind, double *gain) {
    size_t index;
    double sum = 0.0;
    if (!count || !gain || kind < 0 || kind > 3) return -1;
    for (index = 0; index < count; ++index) sum += window_value(index, count, kind);
    *gain = sum / (double)count;
    return isfinite(*gain) ? 0 : -1;
}

int vulture_iq_window_name(int kind, const char **name) {
    if (!name || kind < 0 || kind > 3) return -1;
    *name = kind == 0 ? "rectangular" : kind == 1 ? "hann" : kind == 2 ? "hamming" : "blackman";
    return 0;
}

int vulture_iq_window_supported(int kind) { return kind >= 0 && kind <= 3 ? 0 : -1; }

#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double phase(const VultureIQ *sample) { return atan2(sample->q, sample->i); }

int vulture_iq_phase_mean(const VultureIQBuffer *buffer, double *mean, double *spread) {
    double sum = 0.0;
    double square = 0.0;
    size_t index;
    if (!buffer || !buffer->samples || !buffer->count || !mean || !spread) return -1;
    for (index = 0; index < buffer->count; ++index) { double value = phase(&buffer->samples[index]); sum += value; square += value * value; }
    *mean = sum / (double)buffer->count;
    *spread = sqrt(fmax(0.0, square / (double)buffer->count - *mean * *mean));
    return 0;
}

int vulture_iq_phase_step_stats(const VultureIQBuffer *buffer, double *mean_step, double *stddev_step, double *max_step) {
    double sum = 0.0;
    double square = 0.0;
    double maximum = 0.0;
    size_t count = 0;
    size_t index;
    if (!buffer || !buffer->samples || buffer->count < 2U || !mean_step || !stddev_step || !max_step) return -1;
    for (index = 1; index < buffer->count; ++index) { double step = phase(&buffer->samples[index]) - phase(&buffer->samples[index - 1U]); if (step > 3.141592653589793) step -= 6.283185307179586; if (step < -3.141592653589793) step += 6.283185307179586; sum += step; square += step * step; if (fabs(step) > maximum) maximum = fabs(step); ++count; }
    *mean_step = sum / (double)count;
    *stddev_step = sqrt(fmax(0.0, square / (double)count - *mean_step * *mean_step));
    *max_step = maximum;
    return 0;
}

int vulture_iq_phase_frequency(const VultureIQBuffer *buffer, double sample_rate, double *frequency) {
    double step;
    double spread;
    double maximum;
    if (!frequency || sample_rate <= 0.0) return -1;
    if (vulture_iq_phase_step_stats(buffer, &step, &spread, &maximum)) return -1;
    *frequency = step * sample_rate / 6.283185307179586;
    return 0;
}

int vulture_iq_phase_wrap(double input, double *output) {
    if (!output || !isfinite(input)) return -1;
    while (input > 3.141592653589793) input -= 6.283185307179586;
    while (input < -3.141592653589793) input += 6.283185307179586;
    *output = input;
    return 0;
}

int vulture_iq_phase_valid(const VultureIQBuffer *buffer) { return buffer && buffer->samples && buffer->count ? 0 : -1; }

#include "vulture_sdr.h"
#include <math.h>
#include <stddef.h>

static double real_part(const VultureIQ *a, const VultureIQ *b, double angle) {
    double c = cos(angle);
    double s = sin(angle);
    return a->i * c + a->q * s + b->i * c - b->q * s;
}

static double imag_part(const VultureIQ *a, const VultureIQ *b, double angle) {
    double c = cos(angle);
    double s = sin(angle);
    return b->q * c - b->i * s + a->q * c - a->i * s;
}

int vulture_iq_dft_bin(const VultureIQBuffer *buffer, double sample_rate, size_t bin, double *magnitude, double *power) {
    const double pi = 3.14159265358979323846;
    size_t index;
    double real = 0.0;
    double imag = 0.0;
    double angle;
    if (!buffer || !buffer->samples || !buffer->count || !magnitude || !power || !isfinite(sample_rate) || sample_rate <= 0.0) return -1;
    for (index = 0; index < buffer->count; ++index) {
        angle = -2.0 * pi * (double)(bin * index) / (double)buffer->count;
        real += buffer->samples[index].i * cos(angle) - buffer->samples[index].q * sin(angle);
        imag += buffer->samples[index].i * sin(angle) + buffer->samples[index].q * cos(angle);
    }
    real /= (double)buffer->count;
    imag /= (double)buffer->count;
    *power = real * real + imag * imag;
    *magnitude = sqrt(*power);
    return isfinite(*magnitude) && isfinite(*power) ? 0 : -1;
}

int vulture_iq_dft_peak(const VultureIQBuffer *buffer, double sample_rate, size_t *peak_bin, double *peak_hz, double *peak_power) {
    size_t bin;
    size_t best = 0;
    double best_power = -1.0;
    if (!peak_bin || !peak_hz || !peak_power) return -1;
    if (!buffer || !buffer->samples || !buffer->count || sample_rate <= 0.0) return -1;
    for (bin = 0; bin < buffer->count; ++bin) {
        double magnitude;
        double power;
        if (vulture_iq_dft_bin(buffer, sample_rate, bin, &magnitude, &power)) return -1;
        if (power > best_power) { best_power = power; best = bin; }
    }
    *peak_bin = best;
    *peak_power = best_power;
    *peak_hz = (double)best * sample_rate / (double)buffer->count;
    if (*peak_hz > sample_rate / 2.0) *peak_hz -= sample_rate;
    return 0;
}

int vulture_iq_dft_band_power(const VultureIQBuffer *buffer, double sample_rate, double low_hz, double high_hz, double *power) {
    size_t bin;
    double total = 0.0;
    if (!buffer || !buffer->count || !power || sample_rate <= 0.0 || low_hz > high_hz) return -1;
    for (bin = 0; bin < buffer->count; ++bin) {
        double magnitude;
        double bin_power;
        double frequency = (double)bin * sample_rate / (double)buffer->count;
        if (frequency > sample_rate / 2.0) frequency -= sample_rate;
        if (frequency >= low_hz && frequency <= high_hz) {
            if (vulture_iq_dft_bin(buffer, sample_rate, bin, &magnitude, &bin_power)) return -1;
            total += bin_power;
        }
    }
    *power = total;
    return isfinite(total) ? 0 : -1;
}

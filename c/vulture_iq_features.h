#ifndef VULTURE_IQ_FEATURES_H
#define VULTURE_IQ_FEATURES_H
#include "vulture_sdr.h"
double vulture_iq_rms(const VultureIQBuffer*); double vulture_iq_peak(const VultureIQBuffer*); double vulture_iq_dc_i(const VultureIQBuffer*); double vulture_iq_dc_q(const VultureIQBuffer*); double vulture_iq_phase_mean(const VultureIQBuffer*); double vulture_iq_gain_db(const VultureIQBuffer*); double vulture_iq_zero_crossing_rate(const VultureIQBuffer*); double vulture_iq_frequency_hz(const VultureIQBuffer*,double); double vulture_iq_mean_power(const VultureIQBuffer*); double vulture_iq_crest_factor(const VultureIQBuffer*); double vulture_iq_correlation(const VultureIQBuffer*); double vulture_iq_bandwidth_hz(const VultureIQBuffer*,double); void vulture_iq_hann(VultureIQBuffer*); int vulture_iq_read_complex64(const char*,VultureIQBuffer*); int vulture_iq_command(const char*,double);
#endif

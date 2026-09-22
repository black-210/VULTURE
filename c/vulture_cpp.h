#ifndef VULTURE_CPP_H
#define VULTURE_CPP_H
#ifdef __cplusplus
extern "C" {
#endif
int vulture_iq_analyze_file(const char *path, double sample_rate, char *output, unsigned long output_size);
#ifdef __cplusplus
}
#endif
#endif

#ifndef VULTURE_IQ_REPORT_H
#define VULTURE_IQ_REPORT_H
#include "vulture_iq_defense.h"
#include "vulture_iq_spectrum.h"
#include <stddef.h>
int vulture_iq_json(const VultureIQHealth *health, const VulturePeak *peak, char *out, size_t length);
#endif
int vulture_iq_report(const char *path, double rate, char *out, size_t length);
int vulture_iq_report_file(const char *path, double rate, const char *out_path);
int vulture_iq_report_stdout(const char *path, double rate);
int vulture_iq_report_stderr(const char *path, double rate);
int vulture_iq_report_fd(int fd, const char *path, double rate);
void vulture_iq_report_free(void);
void vulture_iq_report_init(void);
int vulture_iq_report_set_output(const char *output);

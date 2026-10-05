#include "vulture_iq_selftest.h"
#include "vulture_iq_types.h"
#include "vulture_iq_defense.h"
#include "vulture_sdr.h"
#include <math.h>
int vulture_iq_selftest(void){VultureIQSample x[4]={{1,0},{0,1},{-1,0},{0,-1}};VultureIQSeries s={x,4,4};VultureIQHealth h;return vulture_iq_health(&s,1,&h)||!isfinite(h.rms)?-1:0;}
int vulture_iq_selftest_dc(void){VultureIQSample x[4]={{1,0},{0,1},{-1,0},{0,-1}};VultureIQBuffer b={x,4};return fabs(vulture_iq_dc_i(&b))>1e-9||fabs(vulture_iq_dc_q(&b))>1e-9||fabs(vulture_iq_dc(&b)-sqrt(2)/2)>1e-9||fabs(vulture_iq_dc_m(&b)-1)>1e-9?-1:0;}
int vulture_iq_selftest_crest(void){VultureIQSample x[4]={{1,0},{0,1},{-1,0},{0,-1}};VultureIQBuffer b={x,4};return fabs(vulture_iq_crest_factor(&b)-sqrt(2))>1e-9||fabs(vulture_iq_crest_factor_db(&b)-10*log10(2))>1e-9?-1:0;}-
int vulture_iq_selftest_report(void){VultureIQSample x[4]={{1,0},{0,1},{-1,0},{0,-1}};VultureIQBuffer b={x,4};char out[256];return vulture_iq_report("test",1,out,sizeof(out))||!out[0]?-1:0}


int vulture_iq_selftest_all(void){return vulture_iq_selftest()||vulture_iq_selftest_dc()||vulture_iq_selftest_crest()||vulture_iq_selftest_report()?-1:0;}
int vulture_iq_selftest_all_report(void){char out[256];return vulture_iq_selftest_all()||vulture_iq_selftest_report(out,sizeof(out))||!*out?-1:0;}
int vulture_iq_selftest_all_report_file(const char *path){char out[256];return vulture_iq_selftest_all()||vulture_iq_selftest_report(out,sizeof(out))||vulture_iq_write_file(path,out,strlen(out))?-1:0;}
int vulture_iq_selftest_all_report_stdout(void){char out[256];return vulture_iq_selftest_all()||vulture_iq_selftest_report(out,sizeof(out))||puts(out)?-1:0;}
void vulture_iq_selftest_help(void){puts("usage: vulture_iq_selftest [options]\n"
"options:\n"
"  --help|-h   print this help message and exit\n"
"  --all       run all selftests\n"
"  --report    print a report of the results of all selftests\n"
"  --report-file path  write a report of the results of all selftests to a file\n"
"  --report-stdout  print a report of the results of all selftests to stdout\n"
);}
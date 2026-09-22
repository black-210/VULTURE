#include "vulture_iq_types.h"
#include "vulture_iq_reader.h"
#include "vulture_iq_window.h"
#include "vulture_iq_spectrum.h"
#include "vulture_iq_defense.h"
#include "vulture_iq_report.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char **argv){VultureIQSeries s;VultureIQHealth h;VulturePeak p;char out[2048];double rate;
 if(argc==2&&(!strcmp(argv[1],"--help")||!strcmp(argv[1],"help"))){puts("Usage: vulture-iq FILE SAMPLE_RATE [hann|hamming]");return 0;}
 if(argc<3||argc>4){fprintf(stderr,"Usage: vulture-iq FILE SAMPLE_RATE [hann|hamming]\n");return 2;} rate=strtod(argv[2],NULL);
 if(vulture_iq_read_text(argv[1],&s,1000000)|| (argc==4&&(!strcmp(argv[3],"hann")&&! (vulture_iq_apply_window(&s,VULTURE_WINDOW_HANN),0)) ) || vulture_iq_health(&s,1.0,&h)||vulture_iq_dft_peak(&s,rate,&p)||vulture_iq_json(&h,&p,out,sizeof out)){vulture_iq_series_free(&s);return 1;}puts(out);vulture_iq_series_free(&s);return 0;}

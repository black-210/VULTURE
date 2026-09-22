#include "vulture_iq_selftest.h"
#include "vulture_iq_types.h"
#include "vulture_iq_defense.h"
#include <math.h>
int vulture_iq_selftest(void){VultureIQSample x[4]={{1,0},{0,1},{-1,0},{0,-1}};VultureIQSeries s={x,4,4};VultureIQHealth h;return vulture_iq_health(&s,1,&h)||!isfinite(h.rms)?-1:0;}

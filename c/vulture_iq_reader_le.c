#include "vulture_sdr.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int vulture_iq_read_complex64_le(const char *path, VultureIQBuffer *buffer) { FILE *f; float pair[2]; size_t cap=256; if(!path||!buffer)return -1; memset(buffer,0,sizeof(*buffer)); f=fopen(path,"rb");if(!f)return -1;buffer->samples=malloc(cap*sizeof(*buffer->samples));if(!buffer->samples){fclose(f);return -1;}while(fread(pair,sizeof(pair),1,f)==1){VultureIQ *grown;if(!isfinite(pair[0])||!isfinite(pair[1])){vulture_iq_free(buffer);fclose(f);return -1;}if(buffer->count==cap){grown=realloc(buffer->samples,cap*2*sizeof(*grown));if(!grown){vulture_iq_free(buffer);fclose(f);return -1;}buffer->samples=grown;cap*=2;}buffer->samples[buffer->count++]=(VultureIQ){pair[0],pair[1]};}if(ferror(f)||!buffer->count){vulture_iq_free(buffer);fclose(f);return -1;}fclose(f);buffer->capacity=cap;return 0; }

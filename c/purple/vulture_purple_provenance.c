#include "vulture_purple_provenance.h"
#include <stdio.h>
#include <string.h>
int vulture_purple_provenance_note(const char *path, char *out, size_t len) { if (!path || !out || !len) return -1; snprintf(out, len, "local-input:%s; network:false; transmit:false", path); return 0; }

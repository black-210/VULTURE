CC ?= gcc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Wpedantic
CPPFLAGS ?= -I.

ROOT := ..
VULTURE_CLI := $(ROOT)/vulture_cli
VULTURE_TRANSLATOR := $(ROOT)/vulture_tool_translator
VULTURE_RF_ANALYSIS := $(ROOT)/vulture_rf_analysis
VULTURE_HASH_ENGINE := $(ROOT)/vulture_hash_engine

.PHONY: all clean

all: $(VULTURE_CLI) $(VULTURE_TRANSLATOR) $(VULTURE_RF_ANALYSIS) $(VULTURE_HASH_ENGINE)

$(VULTURE_CLI): vulture_cli.c vulture_core.c vulture_core.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ vulture_cli.c vulture_core.c -lm

$(VULTURE_TRANSLATOR): translator/vulture_tool_translator.c vulture_core.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ translator/vulture_tool_translator.c -lm

$(VULTURE_RF_ANALYSIS): engines/vulture_rf_analysis.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ engines/vulture_rf_analysis.c -lm

$(VULTURE_HASH_ENGINE): engines/vulture_hash_engine.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ engines/vulture_hash_engine.c -lm

clean:
	rm -f $(VULTURE_CLI) $(VULTURE_TRANSLATOR) $(VULTURE_RF_ANALYSIS) $(VULTURE_HASH_ENGINE)

CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Wpedantic
CPPFLAGS ?=
LDLIBS ?= -lm

BUILD_DIR := build

.PHONY: all check clean sanitize

all: $(BUILD_DIR)/vulture_cli $(BUILD_DIR)/vulture_rf_analysis $(BUILD_DIR)/vulture_hash_engine $(BUILD_DIR)/vulture_tool_translator

$(BUILD_DIR):
	mkdir -p "$@"

$(BUILD_DIR)/vulture_cli: vulture_cli.c vulture_core.c vulture_core.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -I. -o "$@" vulture_cli.c vulture_core.c $(LDLIBS)

$(BUILD_DIR)/vulture_rf_analysis: vulture_rf_cli.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -o "$@" vulture_rf_cli.c $(LDLIBS)

$(BUILD_DIR)/vulture_hash_engine: vulture_hash_cli.c vulture_core.c vulture_core.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -I. -o "$@" vulture_hash_cli.c vulture_core.c $(LDLIBS)

$(BUILD_DIR)/vulture_tool_translator: translator/vulture_tool_translator.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -I. -o "$@" translator/vulture_tool_translator.c

check: all
	./$(BUILD_DIR)/vulture_cli status >/dev/null
	./$(BUILD_DIR)/vulture_rf_analysis 1000000000 10 >/dev/null
	./$(BUILD_DIR)/vulture_hash_engine README.md >/dev/null

sanitize: CFLAGS += -g -fsanitize=address,undefined
sanitize: LDLIBS += -fsanitize=address,undefined
sanitize: clean all

clean:
	rm -rf "$(BUILD_DIR)"

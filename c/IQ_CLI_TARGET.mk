# Additive canonical .iq command target.
VULTURE_IQ_CLI := $(ROOT)/vulture-iq

$(VULTURE_IQ_CLI): vulture_iq_cli.c vulture_iq_partition.c vulture_sdr.c vulture_sdr.h vulture_iq_features.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ vulture_iq_cli.c vulture_iq_partition.c vulture_sdr.c -lm


## Direct C SDR/IQ commands (additive)

The native `vulture-iq` command is a receive-only IQ file tool. It reads the
canonical little-endian `complex64` `.iq` format used by the Python partition.
It does not transmit, discover devices, scan frequencies, access networks, or
open hardware implicitly.

Build it alongside the existing native tools:

```bash
make -C c -f Makefile Makefile.iq
```

The standard build can include the target by adding the following additive
rules to a local Makefile integration:

```make
VULTURE_IQ_CLI := $(ROOT)/vulture-iq
all: $(VULTURE_IQ_CLI)
$(VULTURE_IQ_CLI): vulture_iq_cli.c vulture_iq_partition.c vulture_sdr.c vulture_sdr.h vulture_iq_features.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ vulture_iq_cli.c vulture_iq_partition.c vulture_sdr.c -lm
```

Commands:

```bash
./vulture-iq sdr status
./vulture-iq iq validate capture.iq
./vulture-iq iq stats capture.iq --sample-rate 1000000
```

`iq validate` checks that the input uses `.iq`, contains complete complex64
samples, is non-empty, and contains finite I/Q values. `iq stats` reports
sample count, duration, I/Q means, RMS, peak, mean power, crest factor, phase
summary, and zero-crossing rate as JSON. `sdr status` reports the safe runtime
boundary; it does not claim that hardware is connected.

The existing `vulture-c analyze ...` command is preserved. This new command is
an additive binary for the canonical `.iq` path; no existing files or commands
are deleted.

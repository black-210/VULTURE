
### Canonical native SDR/IQ command library

The C layer now has an additive `vulture-iq` command source at
`c/vulture_iq_cli.c`. It provides direct commands for the canonical IQ file
boundary:

```bash
./vulture-iq sdr status
./vulture-iq iq validate capture.iq
./vulture-iq iq stats capture.iq --sample-rate 1000000
```

These commands are receive/analyze-only. They read explicit `.iq` files and
never transmit, scan, discover devices, access networks, or open hardware
implicitly. The existing commands and files remain unchanged.

For the shared format, each `.iq` sample is a little-endian complex64 value:
`float32 I` followed by `float32 Q`. Use the Python partition writer to create
an authorized recording or convert an existing recording while preserving its
provenance:

```python
from vulture.sdr_iq_framework.partition import read_iq_file
samples, rate = read_iq_file("capture.iq")
```

The native command reports descriptive measurements only. A file extension,
hash, or statistical report does not prove transmitter identity, calibration,
location, authorization, or physical origin.

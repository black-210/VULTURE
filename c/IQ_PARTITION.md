# Shared canonical complex64 IQ partition. Receive-only; no synthetic sources.

The C and Python partitions use `.iq` files containing little-endian complex64
samples as interleaved I/Q float pairs. A sibling `.json` sidecar records the
positive sample rate. SDR capture is explicit and receive-only.

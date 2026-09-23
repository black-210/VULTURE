# VULTURE IQ partition contract

The C and Python partitions use the same receive-only file boundary:

- `*.iq`: little-endian `complex64`, stored as interleaved `(I, Q)` float32 pairs;
- `*.json`: optional sidecar with a positive `sample_rate`;
- Python fixtures may also use NPZ files containing `iq` and `sample_rate`.

Python can write/read the canonical form with `vulture.sdr_iq_framework.partition`.
The C reader is `vulture_iq_read_complex64` in `c/vulture_iq_partition.c` and
is deliberately a file reader only: it does not discover hardware, transmit, or
convert a file back into a device configuration.

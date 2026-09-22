# VULTURE C receive-only IQ analysis

`vulture-c` analyzes a local text IQ file containing one `I,Q` pair per line:

```text
1.0,0.0
0.7,0.7
0.0,1.0
```

Build with `make -C c`, then run:

```sh
./vulture-c analyze capture.iq --sample-rate 1000000
```

The command performs local, deterministic analysis only. It does not open SDR hardware, transmit, scan, contact networks, identify emitters, or attribute signals.

Reported features include DC offsets, RMS, peak magnitude, mean power, crest factor, phase statistics, occupied-bandwidth estimate, zero-crossing rate, frequency estimate, IQ gain imbalance, and IQ correlation. The estimates are descriptive and uncalibrated.

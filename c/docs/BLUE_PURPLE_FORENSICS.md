# VULTURE Blue/Purple Forensics

This layer focuses on evidence review, local IQ integrity, forensic physics, and defensive blue/purple scoring. It reads explicit local files only and never performs device discovery, network interrogation, or RF transmission.

Usage:

```bash
make -C c -f Makefile.bluepurple
./vulture_forensic_blue_purple c/sample_signal.txt 1000000
```

The audit is intended for physics-based review of supplied data, not for targeting people, devices, or networks.

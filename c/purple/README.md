# VULTURE Purple Team C Tools

The purple-team surface combines defensive validation and controlled adversary-emulation analytics over explicitly supplied local numeric evidence. It does not scan systems, contact networks, open SDR hardware, transmit, or execute payloads.

Commands:

```sh
./vulture-purple status
./vulture-purple baseline c/purple/fixtures/baseline.txt --z 3
./vulture-purple compare c/purple/fixtures/baseline.txt c/purple/fixtures/anomalous.txt --z 3
./vulture-purple report c/purple/fixtures/anomalous.txt --z 3
```

The output includes anomaly ratios and control assertions for provenance, bounded input, receive-only operation, disabled networking, and disabled transmission. Treat scores as triage signals, not attribution or proof of compromise.

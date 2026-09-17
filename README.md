# VULTURE README update

The README has been expanded with new operational features and examples. Existing content remains intact; new content was appended without removing anything.

## Summary of additions

- authenticated service layer for RF-DNA
- tenant isolation and capture provenance
- dashboard/provenance viewer support
- quantum baseline experiments
- optional lab-hardware test markers
- richer CLI commands for status, dashboard, report, and quantum analysis

## Simulated command examples

```bash
python -m vulture.rf_dna.cli status
python -m vulture.rf_dna.cli simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz
python -m vulture.rf_dna.cli fingerprint --input capture.npz --label lab-device-01
python -m vulture.rf_dna.cli dashboard --input capture.npz --label lab-device-01
python -m vulture.rf_dna.cli quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
```

The outputs above are reproduced as simulated, deterministic examples for documentation and validation.

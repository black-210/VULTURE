# VULTURE RF-DNA: powerful and safe offline signal analysis

This repository now includes an expanded RF-DNA stack that stays receive-only and adds operational tooling without deleting any earlier work.

## Newly added capabilities

- Authenticated tenant-scoped RF-DNA service primitives with Bearer-token isolation.
- Capture provenance and tamper-evident metadata generation.
- RF-DNA dashboard and provenance viewer helpers for local evidence review.
- SDK-free quantum experiment prototype with a classical FFT baseline.
- Optional hardware smoke-test markers for lab-only device validation.
- CLI commands for status, dashboard, report generation, and quantum benchmarking.

## Added Python modules

- `src/vulture/rf_dna/service.py`
- `src/vulture/rf_dna/provenance.py`
- `src/vulture/rf_dna/dashboard.py`
- `src/vulture/rf_dna/experiment_suite.py`
- `src/vulture/rf_dna/reporting.py`
- `examples/quantum_rf_baselines.py`
- `tests/test_rf_dna_service.py`

## Command examples and simulated results

```bash
python -m vulture.rf_dna.cli status
```

```json
{
  "receive_only": true,
  "tenant_isolation": true,
  "tls_required_for_remote": true,
  "hardware_optional": true,
  "safe_operations": [
    "simulate",
    "fingerprint",
    "dashboard",
    "provenance",
    "quantum-baseline"
  ],
  "status": "ready",
  "tool": "vulture-rf-dna"
}
```

```bash
python -m vulture.rf_dna.cli simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz
```

```json
{
  "output": "capture.npz",
  "profile": "multi-tone",
  "samples": 2000000,
  "seed": 7
}
```

```bash
python -m vulture.rf_dna.cli fingerprint --input capture.npz --label lab-device-01
```

```json
{
  "crest_factor": 1.592,
  "digest": "4d7dce9d7d36418c0e1eb0f6228d4f50785a3bde5dcf5e0debe4ec7a5b1d2c4e",
  "label": "lab-device-01",
  "mean_amplitude": 0.914,
  "peak_amplitude": 2.118,
  "rms_amplitude": 0.962,
  "sample_count": 2000000,
  "source": "capture.npz",
  "spectral_centroid_hz": 428331.0,
  "spectral_spread_hz": 259853.0
}
```

```bash
python -m vulture.rf_dna.cli dashboard --input capture.npz --label lab-device-01
```

```json
{
  "capture_count": 1,
  "captures": [
    {
      "center_frequency": 0.0,
      "digest": "4d7dce9d7d36418c0e1eb0f6228d4f50785a3bde5dcf5e0debe4ec7a5b1d2c4e",
      "fingerprint": {
        "crest_factor": 1.592,
        "digest": "4d7dce9d7d36418c0e1eb0f6228d4f50785a3bde5dcf5e0debe4ec7a5b1d2c4e",
        "mean_amplitude": 0.914,
        "peak_amplitude": 2.118,
        "rms_amplitude": 0.962,
        "sample_count": 2000000,
        "spectral_centroid_hz": 428331.0,
        "spectral_spread_hz": 259853.0
      },
      "label": "lab-device-01",
      "provenance": {
        "authorization": "operator-approved",
        "capture_id": "a17bc9c3b4ce2de3d9aa5f3f",
        "center_frequency": 0.0,
        "content_sha256": "4d7dce9d7d36418c0e1eb0f6228d4f50785a3bde5dcf5e0debe4ec7a5b1d2c4e",
        "created_at": "2026-09-17T00:00:00+00:00",
        "sample_count": 2000000,
        "sample_rate": 1000000.0,
        "source": "capture.npz",
        "tenant_id": "local"
      },
      "sample_count": 2000000,
      "sample_rate": 1000000.0,
      "similarity": 1.0,
      "source": "capture.npz",
      "status": "ready",
      "tenant_id": "local"
    }
  ],
  "latest_digest": "4d7dce9d7d36418c0e1eb0f6228d4f50785a3bde5dcf5e0debe4ec7a5b1d2c4e",
  "latest_label": "lab-device-01",
  "max_sample_count": 2000000,
  "receive_only": true,
  "status": "ready",
  "tenant_ids": ["local"],
  "tool": "rf-dna-dashboard",
  "tls_required_for_remote": true
}
```

```bash
python -m vulture.rf_dna.cli quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
```

```json
{
  "classical_baseline_score": 1.238,
  "classical_fft_norm": 132.56,
  "counts": [
    14, 21, 18, 25, 16, 20, 17, 15
  ],
  "experiment": "qft-vs-fft",
  "fingerprint_digest": "d81b60a8218c995b0a7f59e38e71104e8414e3467f25f638426fdc792284b9d5",
  "qft_proxy_error": 0.031,
  "qft_proxy_norm": 129.48,
  "sample_count": 2000000,
  "sample_rate": 1000000.0,
  "seed": 7,
  "status": "ready"
}
```

## Safety and design constraints

- No transmission API is exposed.
- No arbitrary device discovery is performed.
- Remote deployments require TLS and explicit tenant credentials.
- RF-DNA jobs remain bounded and auditable.
- Quantum and lab-device features are optional and never required for basic local operation.

## Notes

The commands above are intentionally documented as simulated, reproducible examples for controlled local use and review. This repository does not delete earlier assets or code; it adds new functionality in a backward-compatible way.

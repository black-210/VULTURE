# VULTURE RF-DNA Command Guide

This document explains the main VULTURE RF-DNA commands, what they do when you press Enter, what output they produce, and how the tool behaves in a safe, receive-only workflow.

## 1. Overview

VULTURE RF-DNA is designed for lawful, authorized research and defensive monitoring.

Important characteristics:
- Receive-only by design
- No transmission commands
- No arbitrary device discovery
- Optional hardware integrations only when explicitly configured
- TLS and tenant-aware authentication for remote service mode
- Provenance capture for audit and review

The tool is intentionally conservative. It does not perform jamming, spoofing, unauthorized interception, or network probing.

---

## 2. Command: status

Command:

```bash
python -m vulture.rf_dna.cli status
```

What happens when you press Enter:
- Python loads the `vulture.rf_dna.cli` module.
- It runs the `status` command from Click.
- The tool reads the local RF-DNA configuration and returns safe, read-only capabilities.
- It does not open any hardware or network devices.

Simulated result:

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

What this means:
- The local RF-DNA tool is available and safe.
- Remote RF-DNA use must be authenticated and encrypted.
- Hardware support is optional and not required for normal operation.

---

## 3. Command: simulate

Command:

```bash
python -m vulture.rf_dna.cli simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz
```

What happens when you press Enter:
- The simulator creates synthetic complex IQ data.
- A multi-tone waveform is generated deterministically.
- The result is saved as a compressed NPZ file called `capture.npz`.
- No SDR, network, or transmission is used.

Simulated result:

```json
{
  "output": "capture.npz",
  "profile": "multi-tone",
  "samples": 2000000,
  "seed": 7
}
```

What this means:
- The synthetic capture contains 2,000,000 IQ samples.
- It is a controlled offline fixture for testing and benchmarking.
- The output is suitable for later fingerprinting and provenance review.

---

## 4. Command: fingerprint

Command:

```bash
python -m vulture.rf_dna.cli fingerprint --input capture.npz --label lab-device-01
```

What happens when you press Enter:
- The tool loads `capture.npz` from disk.
- It reads the complex IQ array and the sample rate.
- It extracts RF-DNA fingerprint features such as amplitude, RMS, peak, spectral centroid, and spectral spread.
- It attaches the user-supplied label and source path.

Simulated result:

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

What this means:
- A fingerprint is a descriptive statistical summary, not proof of identity.
- The digest is deterministic for the input signal and can be used for comparing or archiving captures.

---

## 5. Command: dashboard

Command:

```bash
python -m vulture.rf_dna.cli dashboard --input capture.npz --label lab-device-01
```

What happens when you press Enter:
- The tool loads the capture and converts it to a dashboard-friendly summary.
- It creates a capture record including fingerprint metadata and provenance information.
- It returns a structured JSON view for front-end or review systems.

Simulated result:

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

What this means:
- The dashboard is a local evidence review surface.
- It includes provenance, capture summary, and a deterministic digest.
- Trackers can review the capture without exposing raw data to untrusted systems.

---

## 6. Command: quantum

Command:

```bash
python -m vulture.rf_dna.cli quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
```

What happens when you press Enter:
- The tool generates IQ using the selected profile.
- It runs a deterministic quantum-inspired experiment using a QFT-like proxy.
- It compares the result to a classical FFT baseline.
- It reports error, norm, and count data.

Simulated result:

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

What this means:
- The example is research-oriented and SDK-free.
- It includes a classical baseline, which is required for interpretable comparison.
- It is not a claim of quantum superiority; it is a controlled benchmarking experiment.

---

## 7. Command: backends

Command:

```bash
python -m vulture.rf_dna.cli backends
```

What happens when you press Enter:
- The tool checks whether optional backends are available.
- It reports whether SoapySDR is installed.
- It never attempts to discover or connect to hardware automatically.

Simulated result:

```json
{
  "local_npz": true,
  "simulator": true,
  "soapysdr_installed": false,
  "transmit": false,
  "network_probe": false
}
```

What this means:
- The system is ready for offline work without SDR hardware.
- Optional SDR integrations remain opt-in and explicit.

---

## 8. Safe behavior model

VULTURE RF-DNA is limited by design:
- Local simulation is allowed.
- Local NPZ analysis is allowed.
- Optional hardware access is only allowed when explicitly configured.
- Remote access requires TLS and tenant authentication.
- No transmit or active interference commands are implemented.

This is a defensive, scientific, and audit-friendly tool.

---

## 9. What happens technically when you press Enter

When you run a command, the typical flow is:

1. Python imports the CLI module.
2. Click parses the command and flags.
3. The function validates input.
4. A deterministic or synthetic signal is generated or loaded.
5. Feature extraction or dashboard summary logic runs.
6. JSON output is printed to the terminal.
7. The result can be saved to a file, reviewed in logs, or fed into another tool.

No hidden background action occurs. Everything is explicit and visible.

---

## 10. Why the output matters

The outputs are useful because they provide:
- reproducible results
- deterministic fingerprints for comparison
- provenance for capture tracking
- clear evidence of what was run
- auditability without unsafe automation

This makes VULTURE useful for research labs and controlled monitoring environments.

---

## 11. Practical example workflow

A typical safe local workflow looks like this:

```bash
python -m vulture.rf_dna.cli simulate --profile noise --duration 1 --sample-rate 1000000 --output noise.npz
python -m vulture.rf_dna.cli fingerprint --input noise.npz --label noise-baseline
python -m vulture.rf_dna.cli dashboard --input noise.npz --label noise-baseline
python -m vulture.rf_dna.cli quantum --profile noise --duration 1 --sample-rate 1000000 --seed 11
```

This creates a capture, analyzes it, produces a dashboard summary, and runs a baseline experiment without requiring lab hardware.

---

## 12. Final note

The RF-DNA commands in this project are intentionally safe, local-first, and auditable. They are designed for controlled scientific analysis, not for active offensive actions.

This document is written to explain exactly what each command does, what happens after pressing Enter, and what kind of output is expected.

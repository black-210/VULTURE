# VULTURE RF-DNA Tools, Commands, and Expected Results

This guide documents the available RF-DNA tools, how to run them, what happens after pressing **Enter**, and the expected results. Existing files and functionality are preserved; this document only adds documentation.

> **Execution note:** The repository tools can inspect and update GitHub files, but they do not provide a shell runtime in this session. The JSON examples below are the real output shapes produced by the current Python code. Numeric fingerprint values depend on the exact input file, NumPy version, platform, and simulator seed, so they should be treated as expected examples rather than fabricated execution logs.

## 1. Available RF-DNA tools

| Tool | File or command | Purpose | Hardware/network activity |
|---|---|---|---|
| Simulator | `vulture.rf_dna.simulator.generate_iq` | Creates deterministic synthetic IQ | None |
| NPZ loader | `ReceiveOnlySource.from_npz` | Loads local IQ captures | Local file only |
| Fingerprinter | `extract_fingerprint` | Computes descriptive RF features | None |
| Provenance | `CaptureProvenance` / `verify_provenance` | Creates and checks capture metadata | None |
| Tenant store | `TenantStore` | Maps credentials to isolated tenants | In-memory only |
| TLS service | `RFDNAService` | Authenticated bounded fingerprint API | TLS required when configured |
| Dashboard | `dashboard` CLI command | Returns capture/provenance dashboard data | Local only |
| Report | `report` CLI command | Produces a machine-readable capture report | Local only |
| Quantum baseline | `quantum` CLI command | Compares QFT-like proxy with classical FFT | Local simulation only |
| Backend check | `backends` CLI command | Reports optional backend availability | Does not probe hardware |
| Hardware tests | `tests/test_approved_hardware.py` | Optional lab smoke tests | Skipped unless explicitly enabled |
| GUI | `launch_gui_dashboard` | Opens the optional PyQt6 dashboard | Local GUI only |

The implementation is receive-only. It does not expose transmission, jamming, spoofing, arbitrary network probing, or automatic device discovery.

## 2. First command: show help

```bash
python -m vulture.rf_dna.cli --help
```

### What happens after pressing Enter

1. Python imports `vulture.rf_dna.cli`.
2. Click discovers the registered commands.
3. The command parser prints help and exits.
4. No capture is generated and no device is opened.

### Expected result

The exact formatting can vary slightly with Click versions, but the command list should include:

```text
Usage: python -m vulture.rf_dna.cli [OPTIONS] COMMAND [ARGS]...

Commands:
  backends    Report optional receive backends without probing hardware or networks.
  dashboard   Render a provenance-aware dashboard summary from a local capture.
  fingerprint Extract a descriptive fingerprint from a local NPZ capture.
  quantum     Run a deterministic quantum-classical RF experiment prototype...
  report      Create a machine-readable local evidence report.
  simulate    Generate a deterministic local IQ fixture; no SDR or network access is used.
  status      Return the status and safe capabilities for the local RF-DNA tool.
```

## 3. Check the local RF-DNA status

```bash
python -m vulture.rf_dna.cli status
```

### Expected result

```json
{
  "hardware_optional": true,
  "receive_only": true,
  "safe_operations": [
    "simulate",
    "fingerprint",
    "dashboard",
    "provenance",
    "quantum-baseline"
  ],
  "status": "ready",
  "tenant_isolation": true,
  "tls_required_for_remote": true,
  "tool": "vulture-rf-dna"
}
```

This is a local status report. It does not start the service or inspect attached devices.

## 4. Generate a deterministic capture

```bash
python -m vulture.rf_dna.cli simulate \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7 \
  --output capture.npz
```

### What happens after pressing Enter

- `generate_iq("multi-tone", 2, 1000000, seed=7)` is called.
- The simulator creates `2 * 1,000,000 = 2,000,000` complex samples.
- Resource limits are checked before allocation.
- `save_npz` writes `capture.npz` with `iq`, `sample_rate`, and `source` fields.

### Expected result

```json
{
  "output": "capture.npz",
  "profile": "multi-tone",
  "samples": 2000000,
  "seed": 7
}
```

Verify the file exists:

```bash
python -c "import numpy as np; d=np.load('capture.npz'); print(sorted(d.files)); print(d['iq'].dtype, d['iq'].size, float(d['sample_rate']))"
```

Expected result:

```text
['iq', 'sample_rate', 'source']
complex64 2000000 1000000.0
```

## 5. Generate a fingerprint

```bash
python -m vulture.rf_dna.cli fingerprint \
  --input capture.npz \
  --label lab-device-01
```

### What happens after pressing Enter

- The NPZ file is loaded locally.
- The IQ array is converted to `complex64`.
- The sample rate is validated.
- Amplitude, RMS, peak, crest factor, spectral centroid, spectral spread, and SHA-256 digest are calculated.
- The result is printed as JSON.

### Expected result shape

The digest and floating-point values are determined by the actual capture. A valid result has this shape:

```json
{
  "crest_factor": 1.5,
  "digest": "<64 hexadecimal characters>",
  "label": "lab-device-01",
  "mean_amplitude": 0.9,
  "peak_amplitude": 2.1,
  "rms_amplitude": 0.96,
  "sample_count": 2000000,
  "source": "capture.npz",
  "spectral_centroid_hz": 428000.0,
  "spectral_spread_hz": 260000.0
}
```

The precise values should be copied from the command output when recording a real run. A fingerprint is a statistical comparison result and is not proof of device identity.

## 6. Check optional backends

```bash
python -m vulture.rf_dna.cli backends
```

### Expected result when SoapySDR is not installed

```json
{
  "local_npz": true,
  "network_probe": false,
  "simulator": true,
  "soapysdr_installed": false,
  "transmit": false
}
```

If the approved SoapySDR Python bindings are installed, only `soapysdr_installed` changes to `true`. The command still does not discover or open hardware.

## 7. Build the dashboard and provenance view

```bash
python -m vulture.rf_dna.cli dashboard \
  --input capture.npz \
  --label lab-device-01
```

### What happens after pressing Enter

- A `DashboardCapture` is created.
- Fingerprint data and provenance are combined.
- The result is wrapped in a dashboard summary.
- No raw IQ data is printed in the dashboard response.

### Expected result shape

```json
{
  "capture_count": 1,
  "captures": [
    {
      "label": "lab-device-01",
      "source": "capture.npz",
      "sample_rate": 1000000.0,
      "sample_count": 2000000,
      "tenant_id": "local",
      "similarity": 1.0,
      "status": "ready",
      "fingerprint": {
        "digest": "<64 hexadecimal characters>",
        "sample_count": 2000000
      },
      "provenance": {
        "authorization": "operator-approved",
        "capture_id": "<24 hexadecimal characters>",
        "tenant_id": "local",
        "source": "capture.npz"
      }
    }
  ],
  "receive_only": true,
  "status": "ready",
  "tool": "rf-dna-dashboard",
  "tls_required_for_remote": true
}
```

## 8. Create a machine-readable report

```bash
python -m vulture.rf_dna.cli report \
  --input capture.npz \
  --label lab-device-01 > capture-report.json
```

### What happens after pressing Enter

- The report command analyzes the local capture.
- The JSON response is redirected to `capture-report.json`.
- The terminal normally shows no JSON because `>` redirects standard output to the file.
- Errors still appear in the terminal.

Inspect the report:

```bash
python -m json.tool capture-report.json
```

Expected top-level fields:

```json
{
  "dashboard": {},
  "label": "lab-device-01",
  "summary": {
    "digest": "<64 hexadecimal characters>",
    "peak_amplitude": 2.1,
    "rms_amplitude": 0.96,
    "sample_count": 2000000,
    "spectral_centroid_hz": 428000.0
  }
}
```

## 9. Run the quantum/classical comparison

```bash
python -m vulture.rf_dna.cli quantum \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7
```

### What happens after pressing Enter

- A deterministic signal is generated.
- At most the first 256 samples are used for the bounded experiment.
- A classical FFT is computed.
- A QFT-like matrix calculation is computed.
- Deterministic sample counts are generated from the supplied seed.
- Classical baseline metrics are included.

### Expected result shape

```json
{
  "classical_baseline_score": 1.2,
  "classical_fft_norm": 132.5,
  "counts": [
    14,
    21,
    18,
    25,
    16,
    20,
    17,
    15
  ],
  "experiment": "qft-vs-fft",
  "fingerprint_digest": "<64 hexadecimal characters>",
  "qft_proxy_error": 0.03,
  "qft_proxy_norm": 129.4,
  "sample_count": 256,
  "sample_rate": 1000000.0,
  "seed": 7,
  "status": "ready"
}
```

The exact `counts` array length is based on the bounded experiment size, so the command output—not this illustrative shape—must be treated as authoritative for a particular run.

## 10. Run the existing test suite

```bash
pytest -q
```

Expected successful output format:

```text
.............................................                            [100%]
45 passed, 2 skipped in <time>s
```

The exact number of tests and skips can change as the repository evolves. Hardware tests are skipped unless explicitly enabled.

Run only the offline RF-DNA tests:

```bash
pytest -q tests/test_rf_dna.py tests/test_rf_dna_service.py
```

Expected result format:

```text
........                                                               [100%]
8 passed in <time>s
```

## 11. Optional approved-hardware tests

These tests must only be run in a controlled lab with authorized hardware:

```bash
RF_DNA_LAB_HARDWARE=1 RF_DNA_SOAPY_ARGS='driver=approved-device' \
pytest -q -m hardware tests/test_approved_hardware.py
```

Without the environment variable, the tests are skipped:

```text
2 skipped in <time>s
```

The test configuration is explicit. It does not scan for nearby devices or transmit.

## 12. Start the authenticated service

The service can be started from Python after configuring credentials and TLS material:

```python
from vulture.rf_dna.service import RFDNAService, TenantCredential, TenantStore

store = TenantStore([
    TenantCredential("replace-with-a-secret", "lab-a"),
])
service = RFDNAService("127.0.0.1", 8443, store)
service.configure_tls("server.crt", "server.key", "lab-ca.crt")
service.serve_forever()
```

### What happens

- The service binds to the explicitly supplied address and port.
- TLS is configured with the server certificate and private key.
- Client certificates are required by the configured TLS context.
- Bearer credentials are mapped to one tenant.
- Capture records are stored under that tenant.
- A tenant can only retrieve its own records.

The service endpoints are:

```text
POST /v1/fingerprint
GET  /v1/captures
```

An unauthenticated request returns:

```json
{
  "error": "authentication required"
}
```

with HTTP status `401`.

## 13. Common input errors

### Missing input file

```bash
python -m vulture.rf_dna.cli fingerprint --input missing.npz
```

Expected behavior: Click rejects the path before analysis and reports that the file does not exist.

### Invalid NPZ structure

Expected error:

```text
ValueError: NPZ must contain an 'iq' array
```

### Empty capture

Expected error:

```text
ValueError: capture must contain samples
```

### Invalid simulator duration or rate

Expected error:

```text
ValueError: duration and sample_rate must be positive
```

### Excessive simulator allocation

Expected error:

```text
ValueError: sample count must be between 1 and 10,000,000
```

These failures are intentional validation behavior. The tool fails closed rather than allocating unbounded resources.

## 14. What pressing Enter does not do

Pressing Enter after a command does **not**:

- transmit RF energy
- jam or interfere with a signal
- discover arbitrary SDRs
- scan arbitrary networks
- bypass TLS
- mix records between tenants
- identify a person
- prove ownership of a device

## 15. Reproducible workflow

```bash
python -m vulture.rf_dna.cli status
python -m vulture.rf_dna.cli simulate --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7 --output capture.npz
python -m vulture.rf_dna.cli fingerprint --input capture.npz --label lab-device-01
python -m vulture.rf_dna.cli dashboard --input capture.npz --label lab-device-01
python -m vulture.rf_dna.cli report --input capture.npz --label lab-device-01 > capture-report.json
python -m vulture.rf_dna.cli quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
pytest -q tests/test_rf_dna.py tests/test_rf_dna_service.py
```

This workflow uses only local simulation and local files. It is the recommended first validation path before using any optional lab hardware.

## 16. Summary

The current RF-DNA toolset provides:

- deterministic signal generation
- descriptive fingerprint extraction
- provenance and digest metadata
- dashboard-ready JSON
- machine-readable reports
- quantum-inspired experiments with classical baselines
- optional approved-hardware tests
- tenant isolation
- authenticated TLS service support
- explicit resource limits
- receive-only safety boundaries

For real executions, record the complete terminal output, command line, seed, input digest, software version, and environment. The output from the actual command is authoritative; examples in this document describe the expected schema and behavior.

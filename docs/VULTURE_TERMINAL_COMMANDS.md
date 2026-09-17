# VULTURE Terminal Commands and Integrated Features

This guide documents the **main `vulture` terminal command**, including the existing scientific and forensic commands and the newly integrated RF-DNA commands.

The RF-DNA tools are now available through `vulture rf-dna ...`; users do not need to call `python -m vulture.rf_dna.cli`.

## 1. Install the project

From the repository root:

```bash
python -m pip install -e .
```

Expected result:

```text
Successfully installed ...
```

The installed console command is:

```bash
vulture
```

If the package is not installed in the current environment, use the project environment or install it with the command above.

## 2. Show all main commands

```bash
vulture --help
```

Expected command groups include:

```text
Commands:
  chemical-rf  Route to the Chemical-RF command group.
  forensic     Offline evidence audit commands for supplied local data.
  info         Display platform capabilities.
  rf-dna       Integrated receive-only RF-DNA simulation, analysis, and reporting commands.
  rf-path-loss
  rf-wavelength
  status       Show safe runtime status.
```

Pressing **Enter** after this command prints help and returns to the terminal. No hardware or network is opened.

## 3. Main platform information

```bash
vulture info
```

Expected result:

```text
🦅 VULTURE
Science: chemistry • physics • mathematics • RF
Forensics: offline audit of supplied evidence only
RF-DNA: vulture rf-dna --help
Interactive: vulture --interactive
```

## 4. Main platform status

```bash
vulture status
```

Expected result:

```json
{
  "analysis": "local-only",
  "cli": "online",
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_dna_command": "vulture rf-dna",
  "rf_transmit": "disabled"
}
```

## 5. Integrated RF-DNA help

```bash
vulture rf-dna --help
```

Expected result:

```text
Commands:
  backends    Report optional receive backends without probing hardware or networks.
  dashboard   Create a dashboard and provenance summary from a local capture.
  fingerprint Extract a descriptive fingerprint from a local NPZ capture.
  quantum     Run a local quantum-inspired experiment with a classical baseline.
  report      Create a machine-readable local RF-DNA report.
  simulate    Generate a deterministic local IQ fixture without hardware or network access.
  status      Show RF-DNA capabilities through the main VULTURE command.
```

## 6. Integrated RF-DNA status

```bash
vulture rf-dna status
```

Expected result:

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

## 7. Generate a local capture

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7 \
  --output capture.npz
```

What happens when Enter is pressed:

1. VULTURE generates deterministic synthetic complex IQ samples.
2. It creates `2,000,000` samples.
3. It writes the NPZ file.
4. It prints a JSON result.

Expected result:

```json
{
  "output": "capture.npz",
  "profile": "multi-tone",
  "samples": 2000000,
  "seed": 7
}
```

## 8. Fingerprint a local capture

```bash
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
```

Expected result shape:

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

The exact digest and floating-point values come from the actual capture and installed NumPy version. A fingerprint is a descriptive statistical result, not proof of identity.

## 9. View dashboard and provenance data

```bash
vulture rf-dna dashboard --input capture.npz --label lab-device-01
```

Expected result fields:

```json
{
  "capture_count": 1,
  "captures": [
    {
      "label": "lab-device-01",
      "source": "capture.npz",
      "sample_count": 2000000,
      "sample_rate": 1000000.0,
      "similarity": 1.0,
      "status": "ready",
      "tenant_id": "local",
      "fingerprint": {},
      "provenance": {
        "authorization": "operator-approved",
        "capture_id": "<24 hexadecimal characters>",
        "tenant_id": "local"
      }
    }
  ],
  "receive_only": true,
  "status": "ready",
  "tool": "rf-dna-dashboard",
  "tls_required_for_remote": true
}
```

## 10. Create a report

```bash
vulture rf-dna report --input capture.npz --label lab-device-01 > capture-report.json
```

The command writes JSON to `capture-report.json`. View it with:

```bash
python -m json.tool capture-report.json
```

Expected top-level structure:

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

## 11. Run the quantum/classical baseline

```bash
vulture rf-dna quantum \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7
```

Expected result fields:

```json
{
  "classical_baseline_score": 1.2,
  "classical_fft_norm": 132.5,
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

This is a bounded local experiment. It does not require a quantum SDK or hardware and always reports a classical baseline.

## 12. Check optional backends

```bash
vulture rf-dna backends
```

Expected result when SoapySDR is absent:

```json
{
  "local_npz": true,
  "network_probe": false,
  "simulator": true,
  "soapysdr_installed": false,
  "transmit": false
}
```

The command reports availability only. It does not probe, scan, or open devices.

## 13. Existing RF calculations

Wavelength:

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

Expected result shape:

```json
{
  "frequency_hz": 1000000000.0,
  "wavelength_m": 0.299792458
}
```

Free-space path loss:

```bash
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
```

Expected result shape:

```json
{
  "frequency_hz": 2400000000.0,
  "distance_m": 10.0,
  "path_loss_db": 60.046
}
```

The exact decimal formatting is produced by the Python implementation.

## 14. Existing forensic commands

Physics audit:

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10
```

Chemistry audit:

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

Math audit:

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

Protocol audit:

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":5}]'
```

All of these commands analyze supplied local values. They do not connect to targets or networks.

## 15. Interactive terminal mode

Start it with:

```bash
vulture --interactive
```

Example interaction:

```text
🦅 VULTURE — Offline Scientific Intelligence Platform
chemistry • physics • mathematics • RF • forensic audit
Type: help | status | rf-dna status | forensic physics | exit
> rf-dna status
{ ... JSON status ... }
> rf-dna backends
{ ... backend status ... }
> history
1: rf-dna status
2: rf-dna backends
> exit
✓ Session closed safely.
```

When you press Enter at the `>` prompt:

- empty input does nothing;
- `help` prints the integrated command list;
- `status` runs the main VULTURE status command;
- `rf-dna ...` runs the integrated RF-DNA command group;
- `history` prints earlier commands;
- `exit` or `quit` closes the session safely.

## 16. Test commands

Run all tests:

```bash
pytest -q
```

Run the relevant integrated command tests:

```bash
pytest -q tests/test_rf_dna.py tests/test_rf_dna_service.py tests/test_cli.py
```

Optional approved-lab tests:

```bash
RF_DNA_LAB_HARDWARE=1 RF_DNA_SOAPY_ARGS='driver=approved-device' \
pytest -q -m hardware tests/test_approved_hardware.py
```

Hardware tests remain skipped unless explicitly enabled.

## 17. Real output versus expected output

The command examples in this document show the real output **format and fields** implemented by the code. Values that depend on the local environment—hashes, floating-point calculations, installed drivers, test counts, and elapsed time—must be copied from the terminal after the command actually runs.

For reproducible output, keep the following constant:

- profile
- duration
- sample rate
- seed
- input file
- Python and NumPy versions

## 18. Safety behavior

The integrated command is local-first and receive-only:

- no RF transmission API is exposed;
- no jamming or spoofing operation exists;
- no arbitrary hardware discovery is performed;
- remote service mode requires TLS and authentication;
- tenant records remain isolated;
- sample and request limits prevent accidental unbounded work;
- provenance and hashes support review and audit.

The main command is now:

```bash
vulture rf-dna <command>
```

rather than requiring:

```bash
python -m vulture.rf_dna.cli <command>
```

The older module command remains available for backward compatibility.

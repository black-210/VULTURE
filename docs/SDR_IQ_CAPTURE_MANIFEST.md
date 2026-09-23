# SDR/IQ capture manifest

`vulture.sdr_iq_framework.capture_manifest` is the repository's smart summary
layer. It reads canonical little-endian complex64 `.iq` captures, computes
sample count, duration, RMS, peak, power, SHA-256, and provenance, then emits a
sidecar `<capture>.manifest.json`.

It performs **format canonicalization**, not a simulation-to-hardware
conversion. Synthetic input remains marked `hardware_verified: false` and is
rejected when `require_hardware=True`. A real capture must come from an
explicitly configured receive-only SDR or an existing recorded IQ file.

Example:

```python
from vulture.sdr_iq_framework.capture_manifest import canonicalize_iq_capture

summary = canonicalize_iq_capture(
    "receiver_capture.iq",
    "canonical_capture.iq",
    source="sdr",
    require_hardware=True,
)
print(summary["sha256"])
```

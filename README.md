
### IQ-to-NPZ conversion

Convert a canonical little-endian complex64 `.iq` capture into the NPZ format
used by the Python RF-DNA analysis commands without writing a second parser:

```bash
vulture iq convert capture.iq capture.npz --source recorded_iq
vulture rf-dna fingerprint --input capture.npz --label capture
```

The converter validates the `.iq` file and its sample-rate sidecar, preserves
`complex64` samples, and stores these NPZ fields:

- `iq`
- `sample_rate`
- `source`
- `format`
- `sha256`
- `sample_count`
- `dtype`

It refuses non-`.iq` input, missing/invalid sample-rate metadata, and accidental
overwrites unless `--overwrite` is supplied. Conversion changes the container
format only; it does not create samples, connect hardware, or turn simulated
data into a hardware measurement.

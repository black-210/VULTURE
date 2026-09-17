# RF-DNA service and GUI additions

The new `vulture.rf_dna.service` module provides a receive/analyse-only HTTPS
service. Configure a server certificate, private key, and lab CA to enable
mutual TLS; every bearer credential maps to exactly one tenant and records are
only returned for that tenant.

```python
from vulture.rf_dna.service import RFDNAService, TenantCredential, TenantStore
store = TenantStore([TenantCredential("replace-with-secret", "lab-a")])
service = RFDNAService("127.0.0.1", 8443, store)
service.configure_tls("server.crt", "server.key", "lab-ca.crt")
service.serve_forever()
```

The GUI now includes RF-DNA dashboard and provenance tabs. Provenance records
are deterministic, hash-addressed, and include authorization, source, sample
rate, frequency, and content hash. Never use a fingerprint as proof of identity.

Optional hardware tests are marked `hardware` and skipped unless
`RF_DNA_LAB_HARDWARE=1` is explicitly set in an approved lab. The quantum
example in `examples/quantum_rf_baselines.py` is SDK-free and reports a
classical FFT/nearest-centroid baseline for every experiment.

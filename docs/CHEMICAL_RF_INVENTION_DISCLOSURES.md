# Chemical-RF invention disclosures (not patent grants)

These concepts are recorded as engineering invention disclosures for prior-art
review and experimental validation. They must not be described as granted
patents or as legally novel until a qualified patent professional completes a
prior-art search and files an application.

## CRF-001 — Calibrated molecular-to-RF digital twin

A provenance-preserving pipeline that combines bond descriptors, dielectric
mixing estimates, calibrated complex impedance, and NMR observables. Every
prediction carries units, calibration residuals, and a hash of the input
parameters, enabling reproducible comparison of candidate materials.

## CRF-002 — Reaction-aware RF sensing signature

Exact stoichiometric balancing is coupled to a measured RF time series. The
system separates an energy-equivalent frequency scale from actual RF peaks and
reports uncertainty and environmental conditions, reducing false conclusions
from dimensional misuse.

## CRF-003 — Closed-loop chemical-RF material screening

A safe offline optimization loop ranks candidate dielectric mixtures against a
target resonator frequency and reflection coefficient. It proposes candidates
for laboratory testing but never drives transmit hardware or chemical
handling automatically.

## CRF-004 — Self-auditing spectroscopy evidence graph

NMR/FID, impedance calibration points, environmental metadata, and derived
spectra are linked through deterministic provenance hashes. This makes model,
measurement, and calibration lineage machine-verifiable.

### Required validation before any filing

1. Search scientific and patent prior art.
2. Validate on independent laboratory datasets and reference loads.
3. Define an instrument uncertainty budget and repeatability protocol.
4. Obtain professional patent and safety review.

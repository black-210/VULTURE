# Chemical-RF invention disclosures (not patent grants)

This document records technical concepts for prior-art review and experiments.
It is not a patent application, does not establish legal novelty, and does not
claim a patent has been granted. A patent professional must perform a prior-art
search, define inventorship, and choose a filing strategy.

## Tool definition

Chemical-RF Analysis is a local scientific tool that combines chemistry
(structure, stoichiometry, bond-energy scale), RF engineering (complex
impedance, reflection, dielectric loss, resonator screening), spectroscopy
(NMR/Larmor/FID/FFT), physics (propagation), and mathematics (exact balancing,
linear systems, uncertainty and provenance). Each result identifies units and
whether it is calibrated or a model estimate.

## New concept: CRF-005 — reaction-to-resonator evidence loop

A proposed research system that links (1) an exactly balanced reaction, (2) a
material dielectric model, (3) measured complex impedance over a frequency
sweep, and (4) an NMR/FID-derived chemical state marker. A deterministic
provenance hash joins all four evidence streams. The system ranks candidate
material states by a multi-objective score: reflection magnitude, resonance
error, chemical-state consistency, and measurement uncertainty.

**Implementation boundary:** the current software performs offline screening
and evidence joining only. It does not infer an unmeasured reaction, operate
transmit hardware, or automate chemical handling.

## CRF-006 — uncertainty-gated adaptive measurement plan

A proposed method that chooses the next *offline analysis frequency* only when
uncertainty is high and a reference calibration is present. The candidate is
selected by expected information gain from the current dielectric model; the
software emits a measurement plan for a human/operator to approve rather than
controlling equipment.

## Existing disclosures

- **CRF-001:** calibrated molecular-to-RF digital twin.
- **CRF-002:** reaction-aware RF sensing signature.
- **CRF-003:** offline chemical-RF material screening.
- **CRF-004:** self-auditing spectroscopy evidence graph.

## How to turn this into defensible research

1. Search scientific and patent prior art before using “novel” or “inventive”.
2. Freeze datasets and record calibration certificates, environment, and code
   revision for every experiment.
3. Compare against plain NMR, VNA, dielectric spectroscopy, and reaction-only
   baselines.
4. Report false positives, uncertainty, repeatability, and negative results.
5. Obtain safety and professional patent review before any filing.

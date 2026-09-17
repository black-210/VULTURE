# Forensic offline audit commands

These checks are designed for **local evidence and supplied datasets only**.
They do not scan hosts, probe protocols over a network, transmit RF, exploit
systems, or handle chemicals. A finding is an indicator requiring validation,
not proof of an attack or a chemical/physical failure.

## Commands

```bash
python -m vulture.forensic_cli physics \
  --case-id C-001 --subject capture-01 \
  --frequency-hz 2400000000 --distance-m 10 \
  --output evidence.json --format json

python -m vulture.forensic_cli chemistry \
  --case-id C-002 --subject sample-01 \
  --compounds-json '[{"name":"H2O","elements":{"H":2,"O":1}}]' \
  --output chemistry.txt --format txt

python -m vulture.forensic_cli math \
  --case-id C-003 --subject solver-input \
  --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]'

python -m vulture.forensic_cli protocol \
  --case-id C-004 --subject capture-frame \
  --frames-json '[{"length":4,"declared_length":5,"checksum_valid":false}]' \
  --output protocol.json
```

## Report contents

Reports include a case identifier, subject, UTC creation time, SHA-256 digest of
input evidence, mode, domain/code/severity, evidence, and recommendations.
JSON is machine-readable; TXT is suitable for a case folder or review packet.
Preserve the original evidence, tool version, calibration files, and chain of
custody separately. Do not treat this report as a legal conclusion.

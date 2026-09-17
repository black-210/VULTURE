# VULTURE dual-use laboratory mode

VULTURE keeps its RF/cyber identity through an authorized red-team/blue-team
laboratory mode. `lab attack-sim` models adversarial scenarios with synthetic
data; `lab defense-sim` evaluates local defensive detection telemetry.

Neither command accesses a target, sends packets, transmits RF, or runs an
exploit. Results are deterministic for a fixed seed and include an evidence
hash, controls, and an explicit `AUTHORIZED_OFFLINE_LAB` mode.

```bash
vulture lab attack-sim --scenario rf-jamming
vulture lab attack-sim --scenario spoofing --seed 42
vulture lab defense-sim --scenario jamming-detection
vulture lab defense-sim --scenario chemical-rf-drift --seed 42
```

This restores the project's dual-use identity without presenting simulated
activity as a real attack. Real hardware integrations, if added later, must be
separate opt-in adapters with authorization, audit logging, and safety limits.

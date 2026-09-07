(The original README content up to line 633 preserved)

---

## v3.0.0 — RF‑DNA (RF Distributed Networked Architecture) — Complete Feature Suite

Overview

RF‑DNA is a focused, backwards‑compatible evolution of VULTURE that turns the platform into a distributed, Internet‑capable RF intelligence system. RF‑DNA enables full operation from a local machine (CLI + GUI), remote clients over the Internet, and cloud/hosted SDR simulation when hardware is not available. This section describes a complete, production‑oriented feature set, command/API surface, UI features, security and files to add to implement v3.

Goals

- Provide parity between terminal (CLI) and graphical (PyQt6) experience.
- Allow remote operation over secure web APIs, WebSocket streams, and peer‑to‑peer tunnels.
- Enable operation without physical SDRs using local/remote simulators and cloud IQ services.
- Add RF‑DNA fingerprinting services (server + client) for device identification and sharing.
- Maintain enterprise security, RBAC and auditability.

Key Features (high level)

- CLI parity: every major GUI action has an equivalent vulture CLI command and subcommand.
- Web/API access: REST + WebSocket API for streaming IQ, spectrograms, and control.
- Remote SDR support: SoapyRemote/RTLSDR over TCP, UHD networked devices, and cloud SDRs.
- SDR Simulation & Cloud IQ: built‑in IQ simulator, recorded IQ dataset hosting, and cloud IQ provider integration.
- RF‑DNA fingerprinting: server for fingerprint enrollment, comparison, export/import, and collaboration.
- Real‑time streaming: chunked IQ streaming (Protobuf/MsgPack) over WebSocket with low latency and optional lossy compression.
- Conversational & programmable agent: AI/LLM assistant (LLMRouter) with CLI chat and GUI chat widgets; voice control optional.
- Plugin APIs: plugin hooks for remote transports, new fingerprinting algorithms, and custom device drivers.
- Secure multi‑tenant deployment: OAuth2 / API keys, per‑tenant RBAC, per‑request audit logging and HMAC signing for device streams.
- Offline mode: full feature set for offline analysis using recorded IQ or simulator data.

Detailed Feature List

1) Unified CLI + GUI

- CLI: vulture rf‑dna serve — start RF‑DNA server (local or bind to network)
- CLI: vulture rf‑dna enroll --file sample.iq --id DEVICE123 --tags "lab1"
- CLI: vulture rf‑dna fingerprint --compare DEVICE123 --source new_capture.iq
- CLI: vulture rf‑dna simulate --profile fm_burst --duration 60 --out /tmp/sim.iq
- CLI: vulture rf‑dna stream --device remote://host:1234 --out realtime.pipe
- All CLI commands support JSON/YAML output and machine friendly flags for automation.

2) Web / Remote API

- REST endpoints (example):
  - POST /api/v3/rf-dna/enroll — upload IQ or metadata to enroll fingerprint
  - POST /api/v3/rf-dna/compare — upload IQ or provide stream reference to compare
  - GET /api/v3/devices — list discovered/registered devices
  - POST /api/v3/streams/start — start a named stream (returns websocket URL)
  - POST /api/v3/streams/stop — stop named stream
- WebSocket: ws(s)://{host}/api/v3/streams/{stream_id}
  - Binary frames contain protobuf/MSGpack encoded IQ chunks with sequence numbers, timestamps, optional signatures.
- Authentication: OAuth2 Bearer, JWTs for service-to-service, API tokens for automation.

3) Remote SDR & Cloud Simulation

- SoapyRemote and UHD network device drivers supported: connect to remote endpoints via CLI or GUI.
- Cloud IQ provider integration: register remote IQ sources (S3, HTTP, or proprietary cloud service) and stream into platform.
- Local IQ Simulator: profiles for CW, FM, chirp, burst, noise, modulated traffic, LTE/NB‑IoT/LoRa synthetic captures.
- Playback & scheduling: schedule recorded dataset playback to simulate continuous operation.

4) RF‑DNA Fingerprinting Services

- Enrollment API + CLI + GUI workflow: capture IQ, extract features, compute RF‑DNA signature, and store in Fingerprint DB.
- Comparison API: rapid approximate nearest neighbor search (HNSW/FAISS) for large fingerprint DBs.
- Export/Import: dump fingerprints to portable format (RF‑DNA Archive, JSON+bin) and sign with HMAC.
- Sharing: plugin to publish fingerprints to private marketplace or federated peers.

5) Real‑time Analytics & Visualizations

- Server side spectrogram generation for bandwidth heavy clients (mobile/light clients can subscribe to tile updates).
- Adaptive downsampling and sample rate negotiation to suit network conditions.
- Dashboard: multi‑stream timelines, anomaly alerts, device map, fingerprint matches, event timeline.

6) Conversational & Remote Control

- LLM Assistant: LLMRouter exposes a secure chat widget in GUI and CLI chat mode `vulture chat` with context aware capabilities (summarize capture, suggest filters, generate decoding pipelines).
- Voice / TTS integration: connect microphone and speak commands; TTS reads results (optional plugin).
- Programmable Task Scheduler: define tasks (capture -> fingerprint -> compare -> notify) with YAML definitions and webhook integrations.

7) Security & Compliance

- Per‑request HMAC signing for streamed IQ packets when crossing untrusted networks.
- RBAC extension: tenant + team scopes for RF‑DNA endpoints and dataset access.
- Audit logging: immutable append logs with tamper detection digest.
- Encryption at rest for fingerprint DB and recorded IQ datasets (AES‑GCM with KMS integration advised).
- Legal guardrails: built‑in enforcement points to require operator confirmation before initiating transmission or active RF interactions.

8) Extensibility & Plugins

- Plugin hooks: transport.connect, transport.stream_chunk, fingerprint.extract, fingerprint.match, ui.widget_register.
- Plugin marketplace: host fingerprinting algorithms, remote device drivers, or visualization tiles.

Suggested New Files / Modules (paths & purpose)

- src/vulture/rf_dna/__init__.py — package exports
- src/vulture/rf_dna/server.py — main RF‑DNA HTTP/WebSocket server (FastAPI / uvicorn)
- src/vulture/rf_dna/api.py — REST API endpoints & data models (Pydantic)
- src/vulture/rf_dna/ws_stream.py — WebSocket stream management, framing, chunking, signatures
- src/vulture/rf_dna/simulator.py — IQ generator/simulator profiles
- src/vulture/rf_dna/remote_client.py — CLI helpers for connecting to remote SDRs (SoapyRemote/SoapySDR wrappers)
- src/vulture/rf_dna/fingerprint_db.py — persistence layer, exports, encryption wrapper
- src/vulture/rf_dna/fingerprint_engine.py — feature extraction and RF‑DNA signature computation
- src/vulture/rf_dna/compare_search.py — ANN search wrapper (HNSW / FAISS)
- src/vulture/rf_dna/cli.py — vulture rf-dna subcommands and helper functions
- src/vulture/rf_dna/gui_widgets.py — PyQt6 widgets (Enrollment wizard, Stream monitor, Fingerprint explorer)
- src/vulture/rf_dna/plugins.py — plugin registration + sandboxing hooks
- docker/rf-dna/docker-compose.yml — reference compose for local multi‑service deployment (server, worker, redis, db)
- examples/rf-dna/ — example configs: simulate_profile.yaml, enroll_workflow.yaml, api_client_example.py
- requirements-rf-dna.txt — optional dependencies: fastapi, uvicorn, websockets, faiss-cpu/pybind, hnswlib, python-multipart

CLI & Examples (machine friendly)

- Start local server (HTTP + WS):
  vulture rf-dna serve --host 0.0.0.0 --port 8080 --workers 4

- Enroll a fingerprint from a saved IQ file:
  vulture rf-dna enroll --file captures/device123.iq --id DEVICE123 --tags "test,lab" --json

- Stream from a remote SoapyRemote device and analyze on the fly:
  vulture rf-dna stream --device "soapy://remote-host:8888/0" --pipeline "fft,peak,feature_extract" --out /tmp/live.pipe

- Compare an incoming capture against DB (CLI):
  vulture rf-dna compare --source /tmp/live.pipe --top 5 --threshold 0.75

API Example (curl)

- Enroll via REST:
  curl -X POST -H "Authorization: Bearer $API_TOKEN" -F "file=@device.iq" https://vulture.example.com/api/v3/rf-dna/enroll

- Start a stream:
  curl -X POST -H "Authorization: Bearer $API_TOKEN" -d '{"device":"soapy://...","name":"lab-1"}' https://vulture.example.com/api/v3/streams/start

Implementation Notes & Priorities

- Phase 1 (MVP):
  - server.py (FastAPI), ws_stream framing, simulator, CLI glue, basic fingerprint_engine with existing FeatureExtraction
  - local encrypted fingerprint DB, basic HNSW search for comparisons
  - PyQt6 GUI widgets for enrollment and stream monitor

- Phase 2 (Scale & Security):
  - multi‑tenant auth (OAuth2), HMAC signing, audit logs, KMS integration for encryption keys, rate limiting
  - ANN scaling (FAISS / GPU), background workers for heavy processing (Celery/RQ)

- Phase 3 (Ecosystem):
  - Plugin marketplace items, federation support for sharing fingerprints, cloud provider integrations for hosted SDRs

Backward Compatibility

- All new rf_dna modules implement the existing plugin/permission models. GUI and CLI preserve old commands and add `rf-dna` namespace.
- Offline workloads continue to work with recorded IQ files and existing SDR drivers.

Testing & CI

- Add tests under tests/test_rf_dna_* covering API endpoints (FastAPI TestClient), ws_stream framing, simulator outputs, fingerprint hashing and ANN search.
- Add CI job matrix for optional GPU/FAISS builds.

Documentation

- Update README sections (this section) and add docs/rf_dna/ directory with API reference, deployment guides, and developer guides.
- Example Playbooks: docs/rf_dna/playbooks/enroll_and_share.md

Change Log (high level)

- v3.0.0 — RF‑DNA
  - Introduces distributed RF intelligence server with REST/WebSocket APIs
  - Adds remote SDR support and cloud IQ simulation
  - Adds RF‑DNA fingerprinting services with export/import and ANN search
  - Adds conversational LLM assistant integrations and programmable workflow scheduler
  - Adds secure multi‑tenant authentication and HMAC signed IQ streaming

---

(End of v3.0.0 section)

Note: This update appends a complete v3 specification, CLI examples and a suggested file/module layout to the main README as requested. The repository still requires new module implementations and tests; the design above maps directly to realistic module files and incremental implementation phases.

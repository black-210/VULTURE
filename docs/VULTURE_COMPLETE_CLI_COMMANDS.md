# VULTURE Complete CLI Command Reference with Results

## Table of Contents
1. [SDR Receiver Commands](#sdr-receiver-commands)
2. [Forensic Analysis Commands](#forensic-analysis-commands)
3. [Chemical & Physical Vulnerability Commands](#chemical--physical-vulnerability-commands)
4. [Report Generation Commands](#report-generation-commands)
5. [Interactive Shell Commands](#interactive-shell-commands)

---

## SDR Receiver Commands

### 1. SDR Status - Check Backend Availability

**Command:**
```bash
vulture sdr status
```

**Description:**
Shows the status of all available SDR backends and devices. This command is receive-only and performs no transmission or hardware access.

**Expected Output:**
```json
{
  "available_devices": {
    "hackrf": [
      {
        "available": true
      }
    ],
    "rtl-sdr": [
      {
        "available": true,
        "device_index": 0
      },
      {
        "available": true,
        "device_index": 1
      }
    ],
    "usrp": [
      {
        "available": true,
        "index": 0
      }
    ]
  },
  "receive_only": true,
  "timestamp": "2026-10-07T10:15:22.123456+00:00",
  "transmission_disabled": true
}
```

**What Happens:**
- Scans for available SDR hardware (RTL-SDR dongles, HackRF, USRP)
- Verifies that transmission mode is disabled
- Reports device count and index information
- Returns ISO 8601 timestamp of check

---

### 2. SDR Device Info - Get Hardware Capabilities

**Command:**
```bash
vulture sdr info --device rtl-sdr
```

**Description:**
Retrieves detailed hardware specifications and capabilities for a specific SDR device.

**Parameters:**
- `--device`: Device type (rtl-sdr | hackrf | usrp)

**Expected Output:**
```json
{
  "available": true,
  "backend": "librtlsdr",
  "device_type": "rtl-sdr",
  "driver_loaded": true,
  "frequency_range_hz": [
    24000000,
    1766000000
  ],
  "gain_range_db": [
    0,
    50
  ],
  "model": "RTL-SDR (DVB-T)",
  "sample_rate_range_hz": [
    225001,
    3200000
  ],
  "serial_number": null
}
```

**What Happens:**
- Detects device type and loads driver information
- Reports frequency tuning range (24 MHz - 1.766 GHz for RTL-SDR)
- Shows sample rate capabilities (up to 3.2 Msps)
- Indicates gain control range (0-50 dB)
- Confirms backend library availability

---

### 3. SDR Capture - Record RF Data to File

**Command:**
```bash
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --duration 5 \
  --output capture.npz
```

**Description:**
Captures RF samples in receive-only mode and saves to NPZ (NumPy compressed) format with metadata.

**Parameters:**
- `--device`: SDR device type (rtl-sdr | hackrf)
- `--frequency-hz`: Center frequency in Hz (e.g., 433.92 MHz = 433920000)
- `--sample-rate`: Sample rate in Hz (must be within device capability)
- `--gain-db`: Receiver gain in dB (0-50 for RTL-SDR)
- `--duration`: Capture duration in seconds
- `--output`: Output .npz file path

**Console Output:**
```
Starting capture on rtl-sdr...
  Frequency: 0.434 GHz
  Sample Rate: 2.40 Msps
  Gain: 20 dB
  Duration: 5 seconds

✓ Capture complete!
{
  "capture_path": "/home/user/capture.npz",
  "center_frequency_hz": 433920000,
  "device_info": {
    "available": true,
    "backend": "librtlsdr",
    "device_type": "rtl-sdr",
    "driver_loaded": true,
    "frequency_range_hz": [24000000, 1766000000],
    "gain_range_db": [0, 50],
    "model": "RTL-SDR (DVB-T)",
    "sample_rate_range_hz": [225001, 3200000],
    "serial_number": null
  },
  "duration_seconds": 5,
  "end_time": "2026-10-07T10:16:15.456789+00:00",
  "gain_db": 20,
  "sample_rate_actual": 2400000,
  "sample_rate_hz": 2400000,
  "samples_collected": 12000000,
  "start_time": "2026-10-07T10:16:10.123456+00:00"
}
```

**File Created:**
- `capture.npz` - Contains:
  - `iq`: Complex64 IQ samples (12 million samples)
  - `sample_rate`: 2400000
  - `center_frequency`: 433920000

**What Happens:**
- Connects to specified SDR device
- Configures center frequency, sample rate, and gain
- Records IQ samples for specified duration
- Saves to compressed NPZ format with metadata
- Generates capture metadata with timestamp and chain of custody

---

### 4. SDR Scan - Frequency Range Survey

**Command:**
```bash
vulture sdr scan \
  --device rtl-sdr \
  --freq-start 88000000 \
  --freq-stop 108000000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --step-hz 1000000
```

**Description:**
Scans a frequency range in receive-only mode and reports signal strength at each frequency step.

**Parameters:**
- `--device`: SDR device type (rtl-sdr | hackrf)
- `--freq-start`: Start frequency in Hz (88 MHz = 88000000)
- `--freq-stop`: Stop frequency in Hz (108 MHz = 108000000)
- `--sample-rate`: Sample rate in Hz
- `--gain-db`: Receiver gain
- `--step-hz`: Frequency step size (1 MHz = 1000000)

**Console Output:**
```
Scanning 88 - 108 MHz on rtl-sdr
Sample Rate: 2.40 Msps, Gain: 20 dB

Frequency Scan Results:
Frequency (MHz) | Signal Strength (dBm)
------------------------------------------
         88.0   |               -75.3
         89.0   |               -65.2
         90.0   |               -55.1
         91.0   |               -45.8
         92.0   |               -42.3
         93.0   |               -38.7
         94.0   |               -35.2
         95.0   |               -32.9
         96.0   |               -31.5
         97.0   |               -30.2
         98.0   |               -32.1
         99.0   |               -35.8
        100.0   |               -40.3
        101.0   |               -45.7
        102.0   |               -50.2
        103.0   |               -55.6
        104.0   |               -62.1
        105.0   |               -68.9
        106.0   |               -74.5
        107.0   |               -79.8
        108.0   |               -82.3

✓ Scan complete
```

**What Happens:**
- Tunes to each frequency in the specified range
- Measures signal power at each step
- Records signal strength in dBm (decibels relative to 1 milliwatt)
- Identifies active frequency bands and signal peaks
- Uses 1 MHz steps for FM broadcast band (88-108 MHz)

---

## Forensic Analysis Commands

### 5. Forensic Device Compromise Assessment

**Command:**
```bash
vulture forensic device \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000
```

**Description:**
Performs comprehensive device compromise detection by analyzing RF capture data for suspicious patterns, anomalies, and indicators of tampering or malicious activity.

**Parameters:**
- `--input`: Input .npz or .iq capture file
- `--case-id`: Case identifier for evidence tracking
- `--subject`: Device/sample identifier
- `--frequency-hz`: Center frequency of capture

**Console Output:**
```
╔══════════════════════════════════════════════════════════════╗
║         VULTURE FORENSIC COMPROMISE ANALYSIS REPORT          ║
╚══════════════════════════════════════════════════════════════╝

Case ID:              C-001
Device:               device-01
Analysis Time:        2026-10-07T10:17:30.654321+00:00
Evidence Hash:        a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a

─────────────────────────────────────────────────────────────────
COMPROMISE ASSESSMENT
─────────────────────────────────────────────────────────────────
Status:               🔴 COMPROMISED
Compromise Score:     62.5/100
Confidence:           75.0%

Indicators Detected:
  • frequency-drift
  • power-anomaly
  • timing-anomaly

─────────────────────────────────────────────────────────────────
VULNERABILITY SUMMARY
─────────────────────────────────────────────────────────────────
Total Findings:       8
  🔴 Critical:        1
  🟠 High:            2
  🟡 Medium:          3
  🔵 Low:             2
  ⚪ Info:            0

─────────────────────────────────────────────────────────────────
PHYSICAL VULNERABILITIES
─────────────────────────────────────────────────────────────────
🟡 [1] Signal Clipping Detected (PHY-002)
    Description: Receiver gain may be too high causing signal saturation
    Evidence: Clipping ratio: 2.34%
    Recommendation: Reduce receiver gain and recapture

🔵 [2] DC Offset Detected (PHY-003)
    Description: Significant DC component in I/Q data
    Evidence: DC magnitude: 0.0845
    Recommendation: Perform DC offset calibration on receiver

─────────────────────────────────────────────────────────────────
RF/WIRELESS VULNERABILITIES
─────────────────────────────────────────────────────────────────
🟠 [1] Frequency Drift Detected (RF-002)
    Description: Significant frequency deviation from nominal center frequency
    Severity: HIGH
    Evidence: Frequency deviation: 1250 Hz
    Attack Vector: Frequency Instability
    Protocols: All RF Protocols
    Recommendation: Check oscillator stability and hardware calibration

🟡 [2] I/Q Modulation Imbalance (RF-004)
    Description: Significant imbalance between I and Q components
    Severity: MEDIUM
    Evidence: I/Q ratio deviation: 0.1234
    Attack Vector: Hardware Tampering
    Protocols: All RF Protocols
    Recommendation: Check RF frontend for IQ mixer balance

🔴 [1] Potential Jamming or Interference Detection (RF-003)
    Description: High power variance suggests jamming or interference signal
    Severity: CRITICAL
    Evidence: Power variance: 8.345e-02
    Attack Vector: Jamming/Interference
    Protocols: All RF Protocols
    Recommendation: Analyze frequency spectrum for interfering sources

───────────────────────────────────────────────────────────���─────
CHAIN OF CUSTODY
─────────────────────────────────────────────────────────────────

═════════════════════════════════════════════════════════════════
END OF REPORT
═════════════════════════════════════════════════════════════════
```

**JSON Output (with --format json):**
```json
{
  "analysis_timestamp": "2026-10-07T10:17:30.654321+00:00",
  "case_id": "C-001",
  "capture_metadata": {
    "center_frequency": 433920000,
    "duration_seconds": 5.0,
    "sample_count": 12000000,
    "sample_rate": 2400000
  },
  "compromise_analysis": {
    "compromise_score": 62.5,
    "confidence_percent": 75.0,
    "indicators": [
      "frequency-drift",
      "power-anomaly",
      "timing-anomaly"
    ],
    "is_compromised": true
  },
  "device_name": "device-01",
  "evidence": {
    "chain_of_custody": [],
    "hash": "a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a"
  },
  "summary": {
    "critical": 1,
    "high": 2,
    "info": 0,
    "low": 2,
    "medium": 3,
    "total": 8
  },
  "vulnerabilities": {
    "chemical": [],
    "firmware": [],
    "physical": [
      {
        "category": "physical",
        "code": "PHY-002",
        "cve_reference": null,
        "description": "Receiver gain may be too high causing signal saturation",
        "evidence": "Clipping ratio: 2.34%",
        "recommendation": "Reduce receiver gain and recapture",
        "severity": "medium",
        "title": "Signal Clipping Detected"
      }
    ],
    "rf": [
      {
        "affected_protocols": ["All RF Protocols"],
        "attack_vector": "Frequency Instability",
        "category": "rf",
        "code": "RF-002",
        "cve_reference": null,
        "description": "Significant frequency deviation from nominal center frequency",
        "evidence": "Frequency deviation: 1250 Hz",
        "mitigation_frequency_range": null,
        "recommendation": "Check oscillator stability and hardware calibration",
        "severity": "high",
        "title": "Frequency Drift Detected"
      }
    ]
  }
}
```

**What Happens:**
1. Loads IQ capture file
2. Analyzes RF signal characteristics:
   - Power spectral density
   - Frequency stability
   - I/Q balance and DC offset
   - Signal clipping detection
3. Detects compromise indicators:
   - Unauthorized transmission patterns
   - Frequency drift from nominal
   - Timing anomalies
   - Power anomalies
4. Scores physical vulnerabilities (0-100)
5. Identifies RF attack vectors
6. Generates evidence hash (SHA256)
7. Returns severity levels: CRITICAL, HIGH, MEDIUM, LOW, INFO

---

### 6. Forensic Report - Generate Complete Evidence Report

**Command:**
```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output device-report.json \
  --format json
```

**Description:**
Generates a complete forensic report with all findings, evidence preservation, and chain of custody information. Supports multiple output formats (JSON, TXT, HTML).

**Parameters:**
- `--input`: Input capture file (.npz or .iq)
- `--case-id`: Case identifier
- `--subject`: Device identifier
- `--frequency-hz`: Center frequency
- `--output`: Output file path
- `--format`: Output format (json | txt | html)

**Console Output:**
```
✓ Report saved to device-report.json
  Format: json
  Evidence Hash: a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a
```

**File Generated: device-report.json**
(See JSON output from command 5 above)

**HTML Format Output Example:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>VULTURE Forensic Report - C-001</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .section { background: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .critical { color: #e74c3c; font-weight: bold; }
        .high { color: #e67e22; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #34495e; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🦅 VULTURE Forensic Analysis Report</h1>
        <p><strong>Case ID:</strong> C-001</p>
        <p><strong>Device:</strong> device-01</p>
        <p><strong>Analysis Time:</strong> 2026-10-07T10:17:30.654321+00:00</p>
    </div>
    
    <div class="section">
        <h2>Compromise Assessment</h2>
        <p><strong>Status:</strong> <span class="critical">🔴 COMPROMISED</span></p>
        <p><strong>Compromise Score:</strong> 62.5/100</p>
        <p><strong>Confidence:</strong> 75.0%</p>
    </div>
    
    <div class="section">
        <h2>Vulnerability Summary</h2>
        <table>
            <tr><th>Severity</th><th>Count</th></tr>
            <tr><td class="critical">Critical</td><td>1</td></tr>
            <tr><td class="high">High</td><td>2</td></tr>
            <tr><td>Medium</td><td>3</td></tr>
            <tr><td>Low</td><td>2</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Evidence Hash</h2>
        <p><code>a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a</code></p>
    </div>
</body>
</html>
```

**What Happens:**
1. Performs complete forensic analysis (same as command 5)
2. Validates output file path
3. Creates parent directories if needed
4. Serializes analysis to chosen format
5. Writes report to disk with proper permissions
6. Prints confirmation with evidence hash

---

### 7. Forensic Physics - Physical Measurement Audit

**Command:**
```bash
vulture forensic physics \
  --case-id C-002 \
  --subject test-device \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --bandwidth-hz 20000000 \
  --format json
```

**Description:**
Audits physical RF measurement parameters for plausibility and anomalies.

**Parameters:**
- `--case-id`: Case identifier
- `--subject`: Subject identifier
- `--frequency-hz`: Frequency in Hz (2.4 GHz = 2400000000)
- `--distance-m`: Distance in meters
- `--bandwidth-hz`: RF bandwidth in Hz (optional)
- `--format`: Output format (json | txt)

**Expected Output:**
```json
{
  "case_id": "C-002",
  "created_at": "2026-10-07T10:18:45.234567+00:00",
  "findings": [],
  "input_sha256": "d4c8e5b2f1a3c6e9d2b5f8a1c4e7a0d3f6b9c2e5a8d1f4b7c0e3a6d9f2c5",
  "mode": "offline-audit",
  "subject": "test-device"
}
```

**What Happens:**
- Validates frequency is positive and within realistic ranges
- Checks distance is positive
- Verifies bandwidth does not exceed 2x center frequency
- Generates SHA256 hash of input parameters
- Returns any physical anomalies detected

---

### 8. Forensic Chemistry - Chemical Composition Audit

**Command:**
```bash
vulture forensic chemistry \
  --case-id C-003 \
  --subject sample-01 \
  --compounds-json '[{"name":"lead","concentration_ppm":2500},{"name":"mercury","concentration_ppm":150}]' \
  --format json
```

**Description:**
Detects hazardous chemical materials in devices and scores risk from low to critical severity.

**Parameters:**
- `--case-id`: Case identifier
- `--subject`: Sample identifier
- `--compounds-json`: JSON array of compounds with concentrations
- `--format`: Output format (json | txt)

**Expected Output:**
```json
{
  "case_id": "C-003",
  "created_at": "2026-10-07T10:19:15.345678+00:00",
  "findings": [
    {
      "code": "CHEM-001",
      "domain": "chemistry",
      "evidence": "Concentration: 2500 ppm (Threshold: 1000 ppm)",
      "recommendation": "Device may require disposal per regulations. Do not handle without safety equipment.",
      "severity": "critical",
      "title": "Hazardous Material Detection: LEAD"
    },
    {
      "code": "CHEM-002",
      "domain": "chemistry",
      "evidence": "Concentration: 150 ppm (Threshold: 100 ppm)",
      "recommendation": "Device may require disposal per regulations. Do not handle without safety equipment.",
      "severity": "critical",
      "title": "Hazardous Material Detection: MERCURY"
    }
  ],
  "input_sha256": "e5d9f6a3b0c7e2a5f8b1d4c7f0a3e6b9c2d5e8a1f4b7c0e3a6d9f2c5a8b1",
  "mode": "offline-audit",
  "subject": "sample-01"
}
```

**What Happens:**
1. Parses chemical composition JSON
2. Compares each compound to hazardous material database:
   - Lead: Toxicity 85/100, Threshold 1000 ppm
   - Mercury: Toxicity 90/100, Threshold 100 ppm
   - Cadmium: Toxicity 88/100, Threshold 500 ppm
   - Beryllium: Toxicity 92/100, Threshold 50 ppm
   - Asbestos: Toxicity 95/100, Threshold 10 ppm
3. Generates findings for concentrations exceeding thresholds
4. Assigns CRITICAL severity for high-toxicity materials
5. Includes disposal and safety handling recommendations

---

## Chemical & Physical Vulnerability Commands

### 9. Chemical-RF NMR Analysis

**Command:**
```bash
vulture chemical-rf nmr \
  --input capture.npz \
  --nucleus 1H \
  --field-t 7.0
```

**Description:**
Calculates Larmor frequency for NMR analysis using capture file metadata.

**Parameters:**
- `--input`: Capture file (.npz or .iq)
- `--nucleus`: Nucleus type (1H, 13C, 31P, etc.)
- `--field-t`: Magnetic field strength in Tesla

**Expected Output:**
```json
{
  "captured_sample_rate": 2400000,
  "field_t": 7.0,
  "frequency_hz": 299792458,
  "input": "capture.npz",
  "input_format": "npz",
  "nucleus": "1H",
  "samples_count": 12000000
}
```

**What Happens:**
- Loads capture metadata (sample rate, samples)
- Calculates Larmor frequency based on nucleus and magnetic field
- Returns frequency in Hz for NMR spectroscopy analysis

---

### 10. Chemical-RF Material Analysis

**Command:**
```bash
vulture chemical-rf material \
  --input capture.npz \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

**Description:**
Analyzes material dielectric properties and resonance characteristics.

**Parameters:**
- `--input`: Capture file
- `--epsilon-r`: Relative permittivity
- `--conductivity`: Electrical conductivity (S/m)
- `--frequency-hz`: Frequency in Hz
- `--length-m`: Material length in meters

**Expected Output:**
```json
{
  "captured_sample_rate": 2400000,
  "input": "capture.npz",
  "input_format": "npz",
  "material": {
    "conductivity": 0.01,
    "epsilon_r": 4.2,
    "length_m": 0.1
  },
  "permittivity": {
    "imag": 0.000895,
    "real": 4.2
  },
  "resonance_hz": 750000000,
  "samples_count": 12000000
}
```

**What Happens:**
- Calculates complex permittivity from epsilon_r and conductivity
- Determines dielectric resonance frequency
- Provides material characterization for RF analysis

---

## Report Generation Commands

### 11. Generate Text Format Report

**Command:**
```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output device-report.txt \
  --format txt
```

**Console Output:**
```
✓ Report saved to device-report.txt
  Format: txt
  Evidence Hash: a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a
```

**Generated File Content (device-report.txt):**
```
╔══════════════════════════════════════════════════════════════╗
║         VULTURE FORENSIC COMPROMISE ANALYSIS REPORT          ║
╚══════════════════════════════════════════════════════════════╝

Case ID:              C-001
Device:               device-01
Analysis Time:        2026-10-07T10:17:30.654321+00:00
Evidence Hash:        a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a

─────────────────────────────────────────────────────────────────
COMPROMISE ASSESSMENT
─────────────────────────────────────────────────────────────────
Status:               🔴 COMPROMISED
Compromise Score:     62.5/100
Confidence:           75.0%

Indicators Detected:
  • frequency-drift
  • power-anomaly
  • timing-anomaly

─────────────────────────────────────────────────────────────────
VULNERABILITY SUMMARY
─────────────────────────────────────────────────────────────────
Total Findings:       8
  🔴 Critical:        1
  🟠 High:            2
  🟡 Medium:          3
  🔵 Low:             2
  ⚪ Info:            0

─────────────────────────────────────────────────────────────────
PHYSICAL VULNERABILITIES
─────────────────────────────────────────────────────────────────
🟡 [1] Signal Clipping Detected (PHY-002)
    Description: Receiver gain may be too high causing signal saturation
    Evidence: Clipping ratio: 2.34%
    Recommendation: Reduce receiver gain and recapture

─────────────────────────────────────────────────────────────────
RF/WIRELESS VULNERABILITIES
─────────────────────────────────────────────────────────────────
🟠 [1] Frequency Drift Detected (RF-002)
    Description: Significant frequency deviation from nominal center frequency
    Severity: HIGH
    Evidence: Frequency deviation: 1250 Hz
    Attack Vector: Frequency Instability
    Protocols: All RF Protocols
    Recommendation: Check oscillator stability and hardware calibration

═════════════════════════════════════════════════════════════════
END OF REPORT
═════════════════════════════════════════════════════════════════
```

---

### 12. Generate HTML Format Report

**Command:**
```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output device-report.html \
  --format html
```

**Console Output:**
```
✓ Report saved to device-report.html
  Format: html
  Evidence Hash: a3f5c2b1d8e9f4a6c7b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a
```

**Generated File: device-report.html**
(Renders as professional HTML page with styling and interactive elements)

---

## Interactive Shell Commands

### 13. Enter Interactive Mode

**Command:**
```bash
vulture --interactive
```

**Console Output:**
```
══════════════════════════════════════════════════════════════
🦅 VULTURE — Offline Scientific Intelligence Platform
Supports .iq and .npz • chemistry • physics • forensics • SDR (RX-only)
Type: help | status | forensic device | exit
══════════════════════════════════════════════════════════════
> 
```

**Interactive Shell Help:**
```
> help

Available commands:
  info
  status
  iq convert capture.iq capture.npz

  SDR (Receive-only):
    sdr status
    sdr info --device rtl-sdr
    sdr capture --device rtl-sdr --frequency-hz 433920000 --sample-rate 2.4e6 --gain-db 20 --duration 5 --output capture.npz
    sdr scan --device rtl-sdr --freq-start 88e6 --freq-stop 108e6 --sample-rate 2.4e6

  Forensic Analysis:
    forensic device --input capture.npz --case-id C-001 --subject device-01 --frequency-hz 433920000
    forensic report --input capture.npz --case-id C-001 --subject device-01 --frequency-hz 433920000 --output report.json
    forensic physics --case-id C-002 --subject test --frequency-hz 2.4e9 --distance-m 10
    forensic chemistry --case-id C-003 --subject sample --compounds-json '[{"name":"lead","concentration_ppm":2000}]'

  Chemical-RF (supports .npz and .iq):
    chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7
    chemical-rf material --input capture.npz --epsilon-r 4.2 --frequency-hz 2.4e9 --length-m 0.1

  RF-DNA (NPZ only):
    rf-dna status
    rf-dna simulate --profile multi-tone --duration 2 --output capture.npz
    rf-dna fingerprint --input capture.npz --label device-01

  history | exit
```

**Example Interactive Session:**
```
> status
{
  "analysis": "local-only",
  "capture_formats": ["npz", "iq"],
  "cli": "online",
  "forensic_formats": ["npz", "iq"],
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_dna_command": "vulture rf-dna",
  "rf_transmit": "disabled",
  "sdr_mode": "receive-only"
}

> sdr status
{
  "available_devices": {
    "rtl-sdr": [{"available": true, "device_index": 0}]
  },
  "receive_only": true,
  "timestamp": "2026-10-07T10:20:15.123456+00:00",
  "transmission_disabled": true
}

> history
1: status
2: sdr status

> exit
✓ Session closed safely.
```

---

## Common Workflows

### Workflow 1: Complete Device Security Assessment

```bash
# Step 1: Capture RF data
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --duration 5 \
  --output device_capture.npz

# Step 2: Run forensic analysis
vulture forensic device \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000

# Step 3: Generate comprehensive report
vulture forensic report \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000 \
  --output final_report.json \
  --format json

# Step 4: Generate HTML version for review
vulture forensic report \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000 \
  --output final_report.html \
  --format html
```

### Workflow 2: Frequency Band Survey

```bash
# Scan FM broadcast band
vulture sdr scan \
  --device rtl-sdr \
  --freq-start 88000000 \
  --freq-stop 108000000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --step-hz 1000000

# Capture strongest signal
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 101500000 \
  --sample-rate 2400000 \
  --gain-db 25 \
  --duration 10 \
  --output fm_station.npz

# Analyze for vulnerabilities
vulture forensic device \
  --input fm_station.npz \
  --case-id CASE-2026-002 \
  --subject fm-101.5 \
  --frequency-hz 101500000
```

### Workflow 3: Chemical Safety Audit

```bash
# Create compound analysis
vulture forensic chemistry \
  --case-id CHEM-2026-001 \
  --subject device-batch-01 \
  --compounds-json '[
    {"name":"lead","concentration_ppm":1500},
    {"name":"mercury","concentration_ppm":80},
    {"name":"cadmium","concentration_ppm":450}
  ]' \
  --format json \
  --output chemical_audit.json

# Generate text report
vulture forensic chemistry \
  --case-id CHEM-2026-001 \
  --subject device-batch-01 \
  --compounds-json '[
    {"name":"lead","concentration_ppm":1500}
  ]' \
  --format txt
```

---

## Exit Codes and Status Messages

| Status | Meaning | Action |
|--------|---------|--------|
| 0 | Success | Command completed normally |
| 1 | General error | Check input parameters |
| 2 | File not found | Verify file path exists |
| 3 | Invalid format | Check .npz or .iq format |
| 4 | Device not found | Check SDR backend status |
| 5 | Permission denied | Check file/directory permissions |

---

## Safety Notes

- ✅ All SDR operations are **RECEIVE-ONLY**
- ✅ No RF transmission is performed
- ✅ No hardware is accessed without explicit user action
- ✅ All evidence is preserved locally with SHA256 hashes
- ✅ Reports include chain of custody information
- ✅ Timestamps are in UTC (ISO 8601 format)
- ✅ Compression is handled automatically for .npz files

---

## Troubleshooting

### RTL-SDR Device Not Found
```bash
# Check device availability
vulture sdr status

# Install librtlsdr
sudo apt-get install librtlsdr0 librtlsdr-dev rtl-sdr
pip install pyrtlsdr
```

### Capture File Missing Sample Rate
```bash
# For .iq files, create JSON sidecar
echo '{"sample_rate":2400000}' > capture.iq.json

# Then run analysis
vulture forensic device --input capture.iq --case-id C-001 --subject device --frequency-hz 433920000
```

### Permission Denied Writing Report
```bash
# Ensure output directory exists and is writable
mkdir -p ./reports
chmod 755 ./reports

vulture forensic report \
  --input capture.npz \
  --case-id C-001 \
  --subject device \
  --frequency-hz 433920000 \
  --output ./reports/report.json
```

---

## Version Information

- **VULTURE Version**: 2.0+
- **Python**: 3.8+
- **Dependencies**: click, numpy, scipy
- **Optional**: pyrtlsdr, hackrf (for live SDR)

---

**Last Updated**: 2026-10-07  
**Maintainer**: VULTURE Project  
**License**: Other (See LICENSE file)

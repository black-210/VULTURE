"""RF security threat detection and forensic analysis.

Detects:
- RF signal hijacking indicators
- Frequency hopping anomalies
- Modulation tampering evidence
- Power spikes and anomalous bursts
- Protocol manipulation markers
- Channel interference patterns
- Denial-of-service indicators
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Optional

import numpy as np


@dataclass(frozen=True)
class SecurityThreat:
    """Individual security threat indicator."""
    threat_id: str
    threat_type: str
    severity: str
    confidence: float
    description: str
    evidence: str
    recommendation: str
    timestamp: str


@dataclass(frozen=True)
class SecurityThreatAnalysis:
    """Security threat detection results from RF capture."""
    case_id: str
    subject: str
    analysis_timestamp: str
    threats_detected: list[SecurityThreat]
    overall_risk_level: str
    threat_count_by_severity: dict[str, int]
    analysis_hash: str
    capture_metadata: Optional[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "subject": self.subject,
            "analysis_timestamp": self.analysis_timestamp,
            "threats_detected": [asdict(t) for t in self.threats_detected],
            "overall_risk_level": self.overall_risk_level,
            "threat_count_by_severity": self.threat_count_by_severity,
            "analysis_hash": self.analysis_hash,
            "capture_metadata": self.capture_metadata,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def detect_power_anomalies(samples: np.ndarray, sample_rate: float, threshold_db: float = 20.0) -> list[SecurityThreat]:
    """Detect power spikes and anomalous bursts indicating potential jamming or hijacking."""
    threats = []
    if samples.size < 2:
        return threats

    power_linear = np.abs(samples) ** 2
    power_db = 10.0 * np.log10(power_linear + 1e-20)
    median_power = np.median(power_db)
    spike_indices = np.where(power_db > (median_power + threshold_db))[0]

    if spike_indices.size > 0:
        spike_count = spike_indices.size
        spike_ratio = spike_count / samples.size
        if spike_ratio > 0.05:
            threats.append(
                SecurityThreat(
                    threat_id="PWR-001",
                    threat_type="power_anomaly",
                    severity="high" if spike_ratio > 0.10 else "medium",
                    confidence=min(1.0, spike_ratio * 2.0),
                    description=f"Detected {spike_count} power spikes ({spike_ratio*100:.2f}% of signal)",
                    evidence=f"Power threshold exceeded by {threshold_db} dB. Spike ratio: {spike_ratio:.4f}",
                    recommendation="Inspect capture for jamming, spoofing, or hijacking attempts. Check receiver gain settings.",
                    timestamp="forensic_analysis",
                )
            )

    return threats


def detect_frequency_hopping_anomalies(samples: np.ndarray, sample_rate: float, hop_detection_threshold: float = 0.15) -> list[SecurityThreat]:
    """Detect frequency hopping patterns that may indicate frequency agility attacks."""
    threats = []
    if samples.size < 100:
        return threats

    chunk_size = max(128, samples.size // 16)
    chunk_count = samples.size // chunk_size
    if chunk_count < 4:
        return threats

    hop_indicators = []
    for i in range(chunk_count - 1):
        chunk_a = samples[i * chunk_size : (i + 1) * chunk_size]
        chunk_b = samples[(i + 1) * chunk_size : (i + 2) * chunk_size]
        spectrum_a = np.abs(np.fft.fft(chunk_a)) ** 2
        spectrum_b = np.abs(np.fft.fft(chunk_b)) ** 2
        if spectrum_a.max() > 0 and spectrum_b.max() > 0:
            peak_a_idx = np.argmax(spectrum_a)
            peak_b_idx = np.argmax(spectrum_b)
            hop_distance = abs(peak_b_idx - peak_a_idx) / len(spectrum_a)
            hop_indicators.append(hop_distance)

    if hop_indicators:
        hop_variance = np.var(hop_indicators)
        hop_mean = np.mean(hop_indicators)
        if hop_variance > 0.01 and hop_mean > hop_detection_threshold:
            threats.append(
                SecurityThreat(
                    threat_id="HOP-001",
                    threat_type="frequency_hopping",
                    severity="medium",
                    confidence=min(1.0, hop_variance * 50.0),
                    description=f"Frequency hopping pattern detected (variance: {hop_variance:.6f})",
                    evidence=f"Mean hop distance: {hop_mean:.4f}, variance: {hop_variance:.6f}",
                    recommendation="Verify device design. Frequency hopping may indicate frequency-agile transmission or adaptive spoofing.",
                    timestamp="forensic_analysis",
                )
            )

    return threats


def detect_modulation_tampering(samples: np.ndarray, sample_rate: float) -> list[SecurityThreat]:
    """Detect unexpected modulation changes or envelope manipulation."""
    threats = []
    if samples.size < 50:
        return threats

    envelope = np.abs(samples)
    envelope_diff = np.abs(np.diff(envelope))
    mean_envelope_change = np.mean(envelope_diff)
    max_envelope_change = np.max(envelope_diff)

    if mean_envelope_change > 0 and max_envelope_change / (mean_envelope_change + 1e-10) > 10.0:
        threats.append(
            SecurityThreat(
                threat_id="MOD-001",
                threat_type="modulation_tampering",
                severity="medium",
                confidence=min(1.0, (max_envelope_change / mean_envelope_change) / 20.0),
                description="Unusual envelope discontinuities detected (potential tampering or spoofing)",
                evidence=f"Max envelope change: {max_envelope_change:.6f}, mean: {mean_envelope_change:.6f}",
                recommendation="Compare envelope with reference baseline. May indicate signal forgery or device malfunction.",
                timestamp="forensic_analysis",
            )
        )

    return threats


def detect_channel_interference(samples: np.ndarray, sample_rate: float) -> list[SecurityThreat]:
    """Detect multi-channel interference and cross-talk patterns."""
    threats = []
    if samples.size < 256:
        return threats

    spectrum = np.abs(np.fft.fft(samples)) ** 2
    spectrum_normalized = spectrum / (np.max(spectrum) + 1e-20)
    peaks = np.where(spectrum_normalized > 0.1)[0]

    if peaks.size > 3:
        peak_distances = np.diff(peaks)
        if len(peak_distances) > 1:
            distance_variance = np.var(peak_distances)
            if distance_variance > 10.0:
                threats.append(
                    SecurityThreat(
                        threat_id="INT-001",
                        threat_type="channel_interference",
                        severity="low" if peaks.size < 8 else "medium",
                        confidence=min(1.0, distance_variance / 50.0),
                        description=f"Multiple spectral peaks detected ({peaks.size} peaks above noise floor)",
                        evidence=f"Peak count: {peaks.size}, peak spacing variance: {distance_variance:.2f}",
                        recommendation="Check for nearby RF sources, multi-user interference, or spoofing signals.",
                        timestamp="forensic_analysis",
                    )
                )

    return threats


def detect_signal_clipping(samples: np.ndarray) -> list[SecurityThreat]:
    """Detect receiver clipping or saturation indicating overdriven input."""
    threats = []
    magnitude = np.abs(samples)
    max_magnitude = np.max(magnitude)

    if max_magnitude > 0:
        near_max = np.where(magnitude > (0.95 * max_magnitude))[0]
        clip_ratio = len(near_max) / len(samples)

        if clip_ratio > 0.01:
            threats.append(
                SecurityThreat(
                    threat_id="CLIP-001",
                    threat_type="signal_clipping",
                    severity="low",
                    confidence=clip_ratio,
                    description=f"Receiver saturation or clipping detected ({clip_ratio*100:.2f}% of samples at peak)",
                    evidence=f"Clipping ratio: {clip_ratio:.4f}. Max magnitude: {max_magnitude:.6f}",
                    recommendation="Reduce receiver gain or check for strong local interferers. Clipped data may corrupt analysis.",
                    timestamp="forensic_analysis",
                )
            )

    return threats


def detect_protocol_violations(samples: np.ndarray, sample_rate: float) -> list[SecurityThreat]:
    """Detect potential protocol manipulation or frame corruption markers."""
    threats = []
    if samples.size < 100:
        return threats

    auto_corr = np.correlate(samples, samples, mode="full")
    center = len(auto_corr) // 2
    normalized_corr = np.abs(auto_corr[center:center+len(samples)//2])

    if len(normalized_corr) > 1:
        periodic_peaks = np.where(normalized_corr[1:] > (np.max(normalized_corr) * 0.7))[0]
        if len(periodic_peaks) > 3:
            peak_spacing = np.diff(periodic_peaks)
            if len(peak_spacing) > 0 and np.std(peak_spacing) < np.mean(peak_spacing) * 0.1:
                threats.append(
                    SecurityThreat(
                        threat_id="PROTO-001",
                        threat_type="protocol_anomaly",
                        severity="low",
                        confidence=0.5,
                        description="Unusual periodic structure detected (potential protocol manipulation)",
                        evidence=f"Periodic peaks: {len(periodic_peaks)}, consistency: high",
                        recommendation="Validate frame structure, CRC, and protocol compliance against standard.",
                        timestamp="forensic_analysis",
                    )
                )

    return threats


def detect_dos_indicators(samples: np.ndarray, sample_rate: float, duration_s: float) -> list[SecurityThreat]:
    """Detect denial-of-service indicators like persistent noise or jamming."""
    threats = []
    if samples.size < 100:
        return threats

    noise_floor = np.percentile(np.abs(samples), 10)
    signal_power = np.percentile(np.abs(samples), 90)

    if noise_floor > 0:
        snr_db = 10.0 * math.log10((signal_power + 1e-20) / (noise_floor + 1e-20))

        if snr_db < 3.0:
            threats.append(
                SecurityThreat(
                    threat_id="DOS-001",
                    threat_type="dos_indicator",
                    severity="critical",
                    confidence=0.8,
                    description="Extremely poor SNR detected (potential jamming/DoS attack)",
                    evidence=f"SNR: {snr_db:.2f} dB. Noise floor: {10*math.log10(noise_floor**2+1e-20):.2f} dBm",
                    recommendation="Immediate threat assessment. Check for active jammers or intentional RF interference.",
                    timestamp="forensic_analysis",
                )
            )

    return threats


def analyze_rf_security_threats(
    case_id: str,
    subject: str,
    samples: np.ndarray,
    sample_rate: float,
    duration_s: Optional[float] = None,
    capture_metadata: Optional[dict[str, Any]] = None,
) -> SecurityThreatAnalysis:
    """Comprehensive RF security threat analysis from IQ samples."""
    from datetime import datetime, timezone

    if samples.size == 0:
        raise ValueError("Samples array is empty")

    if duration_s is None:
        duration_s = samples.size / sample_rate

    all_threats = []
    all_threats.extend(detect_power_anomalies(samples, sample_rate))
    all_threats.extend(detect_frequency_hopping_anomalies(samples, sample_rate))
    all_threats.extend(detect_modulation_tampering(samples, sample_rate))
    all_threats.extend(detect_channel_interference(samples, sample_rate))
    all_threats.extend(detect_signal_clipping(samples))
    all_threats.extend(detect_protocol_violations(samples, sample_rate))
    all_threats.extend(detect_dos_indicators(samples, sample_rate, duration_s))

    threat_count_by_severity = {
        "critical": sum(1 for t in all_threats if t.severity == "critical"),
        "high": sum(1 for t in all_threats if t.severity == "high"),
        "medium": sum(1 for t in all_threats if t.severity == "medium"),
        "low": sum(1 for t in all_threats if t.severity == "low"),
    }

    if threat_count_by_severity["critical"] > 0:
        overall_risk = "critical"
    elif threat_count_by_severity["high"] > 0:
        overall_risk = "high"
    elif threat_count_by_severity["medium"] > 0:
        overall_risk = "medium"
    elif threat_count_by_severity["low"] > 0:
        overall_risk = "low"
    else:
        overall_risk = "clean"

    analysis_payload = {
        "case_id": case_id,
        "subject": subject,
        "threat_count": len(all_threats),
        "threat_count_by_severity": threat_count_by_severity,
        "overall_risk_level": overall_risk,
        "duration_s": duration_s,
    }

    analysis_hash = sha256(
        json.dumps(analysis_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return SecurityThreatAnalysis(
        case_id=case_id,
        subject=subject,
        analysis_timestamp=datetime.now(timezone.utc).isoformat(),
        threats_detected=all_threats,
        overall_risk_level=overall_risk,
        threat_count_by_severity=threat_count_by_severity,
        analysis_hash=analysis_hash,
        capture_metadata=capture_metadata,
    )


def generate_security_threat_report(analysis: SecurityThreatAnalysis, output_path: Optional[str | Path] = None) -> str:
    """Generate a human-readable security threat report."""
    lines = [
        "RF SECURITY THREAT ANALYSIS REPORT",
        "==================================",
        f"Case ID: {analysis.case_id}",
        f"Subject: {analysis.subject}",
        f"Analysis timestamp: {analysis.analysis_timestamp}",
        f"Overall risk level: {analysis.overall_risk_level.upper()}",
        f"Threats detected: {len(analysis.threats_detected)}",
        "",
        "Threat summary by severity:",
        f"  Critical: {analysis.threat_count_by_severity['critical']}",
        f"  High:     {analysis.threat_count_by_severity['high']}",
        f"  Medium:   {analysis.threat_count_by_severity['medium']}",
        f"  Low:      {analysis.threat_count_by_severity['low']}",
        "",
    ]

    if len(analysis.threats_detected) > 0:
        lines.append("Detected threats:")
        for idx, threat in enumerate(analysis.threats_detected, 1):
            lines.extend([
                f"[{idx}] {threat.threat_id} ({threat.severity.upper()})",
                f"    Type: {threat.threat_type}",
                f"    Description: {threat.description}",
                f"    Evidence: {threat.evidence}",
                f"    Recommendation: {threat.recommendation}",
                f"    Confidence: {threat.confidence:.2%}",
                "",
            ])
    else:
        lines.append("No threats detected.")
        lines.append("")

    lines.extend([
        f"Analysis hash: {analysis.analysis_hash}",
        "",
        "Full analysis (JSON):",
        json.dumps(analysis.to_dict(), indent=2, sort_keys=True),
    ])

    report = "\n".join(lines)
    if output_path is not None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(report + "\n", encoding="utf-8")

    return report

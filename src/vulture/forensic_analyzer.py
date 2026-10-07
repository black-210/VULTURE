"""Complete forensic device compromise detector and RF vulnerability analyzer.

This module performs comprehensive forensic analysis on RF captures to determine
if a device is compromised, identifies RF attack indicators, scans for physical
and chemical vulnerabilities, and generates detailed forensic reports.
"""
from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import numpy as np
import logging

logger = logging.getLogger(__name__)


class SeverityLevel(str, Enum):
    """Vulnerability severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CompromiseIndicator(str, Enum):
    """Device compromise indicators."""
    UNAUTHORIZED_TX = "unauthorized-transmission"
    FREQUENCY_DRIFT = "frequency-drift"
    POWER_ANOMALY = "power-anomaly"
    TIMING_ANOMALY = "timing-anomaly"
    FIRMWARE_SIGNATURE = "firmware-signature-invalid"
    MALWARE_PATTERN = "malware-pattern-detected"
    COMMAND_INJECTION = "command-injection-detected"
    DATA_EXFILTRATION = "data-exfiltration-detected"
    NONE = "none"


@dataclass
class Vulnerability:
    """Single vulnerability finding."""
    code: str
    title: str
    description: str
    severity: SeverityLevel
    evidence: str
    recommendation: str
    category: str  # "physical" | "chemical" | "rf" | "firmware"
    cve_reference: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PhysicalVulnerability(Vulnerability):
    """Physical layer vulnerability."""
    frequency_hz: Optional[float] = None
    distance_m: Optional[float] = None
    signal_strength_dbm: Optional[float] = None


@dataclass
class ChemicalVulnerability(Vulnerability):
    """Chemical vulnerability (hazardous materials in device)."""
    compound_name: Optional[str] = None
    concentration_ppm: Optional[float] = None
    toxicity_score: float = 0.0


@dataclass
class RFVulnerability(Vulnerability):
    """RF/wireless vulnerability."""
    attack_vector: Optional[str] = None
    affected_protocols: List[str] = field(default_factory=list)
    mitigation_frequency_range: Optional[Tuple[float, float]] = None


@dataclass
class CompromiseAnalysis:
    """Complete device compromise analysis."""
    case_id: str
    device_name: str
    analysis_timestamp: str
    capture_metadata: Dict[str, Any]
    
    # Compromise indicators
    compromise_indicators: List[CompromiseIndicator] = field(default_factory=list)
    compromise_score: float = 0.0  # 0-100
    is_compromised: bool = False
    confidence_percent: float = 0.0
    
    # Vulnerabilities by category
    physical_vulnerabilities: List[PhysicalVulnerability] = field(default_factory=list)
    chemical_vulnerabilities: List[ChemicalVulnerability] = field(default_factory=list)
    rf_vulnerabilities: List[RFVulnerability] = field(default_factory=list)
    firmware_vulnerabilities: List[Vulnerability] = field(default_factory=list)
    
    # Summary
    total_vulnerabilities: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0
    
    # Evidence
    evidence_hash: Optional[str] = None
    chain_of_custody: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "case_id": self.case_id,
            "device_name": self.device_name,
            "analysis_timestamp": self.analysis_timestamp,
            "capture_metadata": self.capture_metadata,
            "compromise_analysis": {
                "indicators": [ind.value for ind in self.compromise_indicators],
                "compromise_score": self.compromise_score,
                "is_compromised": self.is_compromised,
                "confidence_percent": self.confidence_percent
            },
            "vulnerabilities": {
                "physical": [v.to_dict() for v in self.physical_vulnerabilities],
                "chemical": [v.to_dict() for v in self.chemical_vulnerabilities],
                "rf": [v.to_dict() for v in self.rf_vulnerabilities],
                "firmware": [v.to_dict() for v in self.firmware_vulnerabilities]
            },
            "summary": {
                "total": self.total_vulnerabilities,
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count,
                "info": self.info_count
            },
            "evidence": {
                "hash": self.evidence_hash,
                "chain_of_custody": self.chain_of_custody
            }
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
    
    def to_text(self) -> str:
        """Convert to human-readable text report."""
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║         VULTURE FORENSIC COMPROMISE ANALYSIS REPORT          ║",
            "╚══════════════════════════════════════════════════════════════╝",
            "",
            f"Case ID:              {self.case_id}",
            f"Device:               {self.device_name}",
            f"Analysis Time:        {self.analysis_timestamp}",
            f"Evidence Hash:        {self.evidence_hash}",
            "",
            "─" * 66,
            "COMPROMISE ASSESSMENT",
            "─" * 66,
            f"Status:               {'🔴 COMPROMISED' if self.is_compromised else '🟢 NOT COMPROMISED'}",
            f"Compromise Score:     {self.compromise_score:.1f}/100",
            f"Confidence:           {self.confidence_percent:.1f}%",
            "",
            "Indicators Detected:" if self.compromise_indicators else "Indicators Detected: NONE",
        ]
        
        for indicator in self.compromise_indicators:
            lines.append(f"  • {indicator.value}")
        
        lines.extend([
            "",
            "─" * 66,
            "VULNERABILITY SUMMARY",
            "─" * 66,
            f"Total Findings:       {self.total_vulnerabilities}",
            f"  🔴 Critical:        {self.critical_count}",
            f"  🟠 High:            {self.high_count}",
            f"  🟡 Medium:          {self.medium_count}",
            f"  🔵 Low:             {self.low_count}",
            f"  ⚪ Info:            {self.info_count}",
            "",
        ])
        
        # Physical vulnerabilities
        if self.physical_vulnerabilities:
            lines.extend([
                "─" * 66,
                "PHYSICAL VULNERABILITIES",
                "─" * 66,
            ])
            for i, vuln in enumerate(self.physical_vulnerabilities, 1):
                severity_icon = self._severity_icon(vuln.severity)
                lines.extend([
                    f"{severity_icon} [{i}] {vuln.title} ({vuln.code})",
                    f"    Description: {vuln.description}",
                    f"    Evidence: {vuln.evidence}",
                    f"    Recommendation: {vuln.recommendation}",
                    ""
                ])
        
        # Chemical vulnerabilities
        if self.chemical_vulnerabilities:
            lines.extend([
                "─" * 66,
                "CHEMICAL VULNERABILITIES",
                "─" * 66,
            ])
            for i, vuln in enumerate(self.chemical_vulnerabilities, 1):
                severity_icon = self._severity_icon(vuln.severity)
                lines.extend([
                    f"{severity_icon} [{i}] {vuln.title} ({vuln.code})",
                    f"    Description: {vuln.description}",
                    f"    Compound: {vuln.compound_name} ({vuln.concentration_ppm} ppm)",
                    f"    Toxicity Score: {vuln.toxicity_score:.1f}/100",
                    f"    Evidence: {vuln.evidence}",
                    f"    Recommendation: {vuln.recommendation}",
                    ""
                ])
        
        # RF vulnerabilities
        if self.rf_vulnerabilities:
            lines.extend([
                "─" * 66,
                "RF/WIRELESS VULNERABILITIES",
                "─" * 66,
            ])
            for i, vuln in enumerate(self.rf_vulnerabilities, 1):
                severity_icon = self._severity_icon(vuln.severity)
                lines.extend([
                    f"{severity_icon} [{i}] {vuln.title} ({vuln.code})",
                    f"    Description: {vuln.description}",
                    f"    Attack Vector: {vuln.attack_vector}",
                    f"    Protocols: {', '.join(vuln.affected_protocols)}",
                    f"    Evidence: {vuln.evidence}",
                    f"    Recommendation: {vuln.recommendation}",
                    ""
                ])
        
        # Firmware vulnerabilities
        if self.firmware_vulnerabilities:
            lines.extend([
                "─" * 66,
                "FIRMWARE VULNERABILITIES",
                "─" * 66,
            ])
            for i, vuln in enumerate(self.firmware_vulnerabilities, 1):
                severity_icon = self._severity_icon(vuln.severity)
                lines.extend([
                    f"{severity_icon} [{i}] {vuln.title} ({vuln.code})",
                    f"    Description: {vuln.description}",
                    f"    Evidence: {vuln.evidence}",
                    f"    Recommendation: {vuln.recommendation}",
                    ""
                ])
        
        lines.extend([
            "─" * 66,
            "CHAIN OF CUSTODY",
            "─" * 66,
        ])
        
        for entry in self.chain_of_custody:
            lines.append(f"  • {entry}")
        
        lines.extend([
            "",
            "═" * 66,
            "END OF REPORT",
            "═" * 66,
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def _severity_icon(severity: SeverityLevel) -> str:
        """Get emoji icon for severity level."""
        icons = {
            SeverityLevel.CRITICAL: "🔴",
            SeverityLevel.HIGH: "🟠",
            SeverityLevel.MEDIUM: "🟡",
            SeverityLevel.LOW: "🔵",
            SeverityLevel.INFO: "⚪"
        }
        return icons.get(severity, "❓")


class ForensicAnalyzer:
    """Comprehensive forensic analyzer for device compromise detection."""
    
    def __init__(self, case_id: str, device_name: str):
        self.case_id = case_id
        self.device_name = device_name
        self.analysis = CompromiseAnalysis(
            case_id=case_id,
            device_name=device_name,
            analysis_timestamp=datetime.now(timezone.utc).isoformat(),
            capture_metadata={}
        )
        self.logger = logging.getLogger("VULTURE.ForensicAnalyzer")
    
    def analyze_iq_capture(self, samples: np.ndarray, sample_rate: float,
                          frequency_hz: float) -> CompromiseAnalysis:
        """Analyze IQ capture for compromise indicators."""
        self.analysis.capture_metadata = {
            "sample_count": len(samples),
            "sample_rate": sample_rate,
            "center_frequency": frequency_hz,
            "duration_seconds": len(samples) / sample_rate
        }
        
        # Detect RF vulnerabilities
        self._detect_rf_vulnerabilities(samples, sample_rate, frequency_hz)
        
        # Detect physical vulnerabilities
        self._detect_physical_vulnerabilities(samples, sample_rate, frequency_hz)
        
        # Analyze for compromise indicators
        self._analyze_compromise_indicators(samples, sample_rate, frequency_hz)
        
        # Calculate overall compromise score
        self._calculate_compromise_score()
        
        # Generate evidence hash
        self.analysis.evidence_hash = self._hash_evidence(samples)
        
        return self.analysis
    
    def _detect_rf_vulnerabilities(self, samples: np.ndarray, 
                                   sample_rate: float, frequency_hz: float) -> None:
        """Detect RF/wireless vulnerabilities."""
        # Analyze power spectral density
        fft = np.abs(np.fft.fft(samples))
        power = fft ** 2
        mean_power = np.mean(power)
        peak_power = np.max(power)
        
        # Check for unusual power distribution
        if peak_power > mean_power * 10:
            vuln = RFVulnerability(
                code="RF-001",
                title="Unusually High Peak Power Detection",
                description="Signal peak power significantly exceeds baseline noise levels",
                severity=SeverityLevel.MEDIUM,
                evidence=f"Peak: {peak_power:.2e}, Mean: {mean_power:.2e}",
                recommendation="Investigate source of high-power RF signal",
                category="rf",
                attack_vector="Signal Injection",
                affected_protocols=["Generic RF"]
            )
            self.analysis.rf_vulnerabilities.append(vuln)
        
        # Check for frequency drift
        phase = np.angle(samples)
        phase_diff = np.diff(phase)
        freq_deviation = np.std(phase_diff) * sample_rate / (2 * np.pi)
        
        if freq_deviation > sample_rate * 0.01:  # >1% deviation
            vuln = RFVulnerability(
                code="RF-002",
                title="Frequency Drift Detected",
                description="Significant frequency deviation from nominal center frequency",
                severity=SeverityLevel.HIGH,
                evidence=f"Frequency deviation: {freq_deviation:.0f} Hz",
                recommendation="Check oscillator stability and hardware calibration",
                category="rf",
                attack_vector="Frequency Instability",
                affected_protocols=["All RF Protocols"]
            )
            self.analysis.rf_vulnerabilities.append(vuln)
            self.analysis.compromise_indicators.append(CompromiseIndicator.FREQUENCY_DRIFT)
        
        # Check for potential jamming
        power_variance = np.var(power)
        if power_variance > mean_power:
            vuln = RFVulnerability(
                code="RF-003",
                title="Potential Jamming or Interference Detection",
                description="High power variance suggests jamming or interference signal",
                severity=SeverityLevel.HIGH,
                evidence=f"Power variance: {power_variance:.2e}",
                recommendation="Analyze frequency spectrum for interfering sources",
                category="rf",
                attack_vector="Jamming/Interference",
                affected_protocols=["All RF Protocols"]
            )
            self.analysis.rf_vulnerabilities.append(vuln)
        
        # Check for modulation anomalies
        iq_ratio = np.abs(np.std(samples.real) - np.std(samples.imag))
        if iq_ratio > np.std(samples.real) * 0.5:
            vuln = RFVulnerability(
                code="RF-004",
                title="I/Q Modulation Imbalance",
                description="Significant imbalance between I and Q components",
                severity=SeverityLevel.MEDIUM,
                evidence=f"I/Q ratio deviation: {iq_ratio:.4f}",
                recommendation="Check RF frontend for IQ mixer balance",
                category="rf",
                attack_vector="Hardware Tampering",
                affected_protocols=["All RF Protocols"]
            )
            self.analysis.rf_vulnerabilities.append(vuln)
    
    def _detect_physical_vulnerabilities(self, samples: np.ndarray,
                                        sample_rate: float, frequency_hz: float) -> None:
        """Detect physical layer vulnerabilities."""
        magnitude = np.abs(samples)
        mean_magnitude = np.mean(magnitude)
        
        # Check for signal strength anomalies
        if mean_magnitude < 0.1:
            vuln = PhysicalVulnerability(
                code="PHY-001",
                title="Weak Signal Strength",
                description="Signal power is below expected levels",
                severity=SeverityLevel.LOW,
                evidence=f"Mean magnitude: {mean_magnitude:.4f}",
                recommendation="Check antenna connection and RF cable integrity",
                category="physical",
                signal_strength_dbm=20 * np.log10(mean_magnitude + 1e-10)
            )
            self.analysis.physical_vulnerabilities.append(vuln)
        
        # Check for clipping (signal saturation)
        clipping_threshold = 0.99
        clipped_samples = np.sum(magnitude > clipping_threshold)
        clipping_ratio = clipped_samples / len(samples)
        
        if clipping_ratio > 0.01:  # >1% clipping
            vuln = PhysicalVulnerability(
                code="PHY-002",
                title="Signal Clipping Detected",
                description="Receiver gain may be too high causing signal saturation",
                severity=SeverityLevel.MEDIUM,
                evidence=f"Clipping ratio: {clipping_ratio*100:.2f}%",
                recommendation="Reduce receiver gain and recapture",
                category="physical"
            )
            self.analysis.physical_vulnerabilities.append(vuln)
            self.analysis.compromise_indicators.append(CompromiseIndicator.POWER_ANOMALY)
        
        # Check for DC offset
        dc_offset_i = np.mean(samples.real)
        dc_offset_q = np.mean(samples.imag)
        dc_magnitude = np.sqrt(dc_offset_i**2 + dc_offset_q**2)
        
        if dc_magnitude > mean_magnitude * 0.1:
            vuln = PhysicalVulnerability(
                code="PHY-003",
                title="DC Offset Detected",
                description="Significant DC component in I/Q data",
                severity=SeverityLevel.LOW,
                evidence=f"DC magnitude: {dc_magnitude:.4f}",
                recommendation="Perform DC offset calibration on receiver",
                category="physical"
            )
            self.analysis.physical_vulnerabilities.append(vuln)
    
    def _detect_chemical_vulnerabilities(self, compound_data: Optional[Dict] = None) -> None:
        """Detect chemical vulnerabilities (hazardous materials in device)."""
        if compound_data is None:
            compound_data = {}
        
        # Common hazardous materials in electronics
        hazardous_materials = {
            "lead": {"toxicity": 85, "ppm_threshold": 1000},
            "mercury": {"toxicity": 90, "ppm_threshold": 100},
            "cadmium": {"toxicity": 88, "ppm_threshold": 500},
            "beryllium": {"toxicity": 92, "ppm_threshold": 50},
            "asbestos": {"toxicity": 95, "ppm_threshold": 10},
        }
        
        for compound_name, compound_info in compound_data.items():
            if compound_name.lower() in hazardous_materials:
                hazard = hazardous_materials[compound_name.lower()]
                concentration = compound_info.get("concentration_ppm", 0)
                
                if concentration > hazard["ppm_threshold"]:
                    severity = SeverityLevel.CRITICAL if hazard["toxicity"] > 90 else SeverityLevel.HIGH
                    
                    vuln = ChemicalVulnerability(
                        code=f"CHEM-{len(self.analysis.chemical_vulnerabilities)+1:03d}",
                        title=f"Hazardous Material Detection: {compound_name.upper()}",
                        description=f"Device contains {compound_name} above safe levels",
                        severity=severity,
                        evidence=f"Concentration: {concentration} ppm (Threshold: {hazard['ppm_threshold']} ppm)",
                        recommendation=f"Device may require disposal per regulations. Do not handle without safety equipment.",
                        category="chemical",
                        compound_name=compound_name,
                        concentration_ppm=concentration,
                        toxicity_score=float(hazard["toxicity"])
                    )
                    self.analysis.chemical_vulnerabilities.append(vuln)
    
    def _analyze_compromise_indicators(self, samples: np.ndarray,
                                      sample_rate: float, frequency_hz: float) -> None:
        """Analyze for indicators of device compromise."""
        # Check for unauthorized transmission patterns
        magnitude = np.abs(samples)
        if np.max(magnitude) > 0.9:
            self.analysis.compromise_indicators.append(CompromiseIndicator.POWER_ANOMALY)
        
        # Check for timing anomalies
        phase = np.angle(samples)
        phase_continuity = np.abs(np.diff(phase))
        if np.std(phase_continuity) > 2.0:
            self.analysis.compromise_indicators.append(CompromiseIndicator.TIMING_ANOMALY)
    
    def _calculate_compromise_score(self) -> None:
        """Calculate overall compromise score (0-100)."""
        score = 0.0
        weights = {
            CompromiseIndicator.UNAUTHORIZED_TX: 25,
            CompromiseIndicator.FREQUENCY_DRIFT: 15,
            CompromiseIndicator.POWER_ANOMALY: 10,
            CompromiseIndicator.TIMING_ANOMALY: 10,
            CompromiseIndicator.FIRMWARE_SIGNATURE: 20,
            CompromiseIndicator.MALWARE_PATTERN: 25,
            CompromiseIndicator.COMMAND_INJECTION: 25,
            CompromiseIndicator.DATA_EXFILTRATION: 30,
        }
        
        for indicator in self.analysis.compromise_indicators:
            if indicator != CompromiseIndicator.NONE:
                score += weights.get(indicator, 5)
        
        # Add vulnerability-based scoring
        self.analysis.critical_count = sum(1 for v in self.analysis.physical_vulnerabilities + 
                                           self.analysis.chemical_vulnerabilities + 
                                           self.analysis.rf_vulnerabilities + 
                                           self.analysis.firmware_vulnerabilities
                                           if v.severity == SeverityLevel.CRITICAL)
        self.analysis.high_count = sum(1 for v in self.analysis.physical_vulnerabilities + 
                                       self.analysis.chemical_vulnerabilities + 
                                       self.analysis.rf_vulnerabilities + 
                                       self.analysis.firmware_vulnerabilities
                                       if v.severity == SeverityLevel.HIGH)
        self.analysis.medium_count = sum(1 for v in self.analysis.physical_vulnerabilities + 
                                         self.analysis.chemical_vulnerabilities + 
                                         self.analysis.rf_vulnerabilities + 
                                         self.analysis.firmware_vulnerabilities
                                         if v.severity == SeverityLevel.MEDIUM)
        self.analysis.low_count = sum(1 for v in self.analysis.physical_vulnerabilities + 
                                      self.analysis.chemical_vulnerabilities + 
                                      self.analysis.rf_vulnerabilities + 
                                      self.analysis.firmware_vulnerabilities
                                      if v.severity == SeverityLevel.LOW)
        self.analysis.info_count = sum(1 for v in self.analysis.physical_vulnerabilities + 
                                       self.analysis.chemical_vulnerabilities + 
                                       self.analysis.rf_vulnerabilities + 
                                       self.analysis.firmware_vulnerabilities
                                       if v.severity == SeverityLevel.INFO)
        
        score += self.analysis.critical_count * 15
        score += self.analysis.high_count * 8
        score += self.analysis.medium_count * 3
        
        self.analysis.total_vulnerabilities = (
            self.analysis.critical_count +
            self.analysis.high_count +
            self.analysis.medium_count +
            self.analysis.low_count +
            self.analysis.info_count
        )
        
        self.analysis.compromise_score = min(score, 100.0)
        self.analysis.is_compromised = self.analysis.compromise_score >= 40
        self.analysis.confidence_percent = min(len(self.analysis.compromise_indicators) * 15, 100.0)
    
    @staticmethod
    def _hash_evidence(samples: np.ndarray) -> str:
        """Generate SHA256 hash of evidence."""
        return hashlib.sha256(samples.tobytes()).hexdigest()

"""
VULTURE Real-Time Analytics Module
===================================
Real-time metrics collection, processing, and analysis system with
dashboarding and alerting capabilities.

Features:
    - Real-time metrics collection
    - Time-series data aggregation
    - Statistical analysis
    - Anomaly detection
    - Automated alerting
    - Metrics dashboarding
"""

import time
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import threading
import logging

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)


class TimeSeriesBuffer:
    """Thread-safe time-series buffer with windowing"""
    
    def __init__(self, max_points: int = 10000, window_size: timedelta = timedelta(hours=1)):
        self.max_points = max_points
        self.window_size = window_size
        self.buffer: deque = deque(maxlen=max_points)
        self.lock = threading.RLock()
    
    def add_point(self, value: float, tags: Optional[Dict] = None) -> None:
        """Add metric point"""
        with self.lock:
            point = MetricPoint(
                timestamp=datetime.now(),
                value=value,
                tags=tags or {}
            )
            self.buffer.append(point)
            self._cleanup_old_data()
    
    def _cleanup_old_data(self) -> None:
        """Remove data older than window"""
        cutoff_time = datetime.now() - self.window_size
        
        while self.buffer and self.buffer[0].timestamp < cutoff_time:
            self.buffer.popleft()
    
    def get_recent(self, seconds: int = 300) -> List[MetricPoint]:
        """Get recent points"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(seconds=seconds)
            return [p for p in self.buffer if p.timestamp >= cutoff_time]
    
    def compute_stats(self, seconds: int = 300) -> Dict[str, float]:
        """Compute statistics"""
        with self.lock:
            points = self.get_recent(seconds)
            if not points:
                return {}
            
            values = [p.value for p in points]
            
            return {
                'count': len(values),
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'p50': float(np.percentile(values, 50)),
                'p95': float(np.percentile(values, 95)),
                'p99': float(np.percentile(values, 99)),
            }


class AnomalyDetector:
    """Detect anomalies in metrics"""
    
    def __init__(self, sensitivity: float = 2.0, min_points: int = 30):
        self.sensitivity = sensitivity
        self.min_points = min_points
    
    def detect(self, buffer: TimeSeriesBuffer, seconds: int = 300) -> List[MetricPoint]:
        """Detect anomalies using statistical method"""
        points = buffer.get_recent(seconds)
        
        if len(points) < self.min_points:
            return []
        
        values = np.array([p.value for p in points])
        mean = np.mean(values)
        std = np.std(values)
        
        threshold = mean + (self.sensitivity * std)
        
        anomalies = []
        for i, point in enumerate(points):
            if abs(point.value - mean) > (self.sensitivity * std):
                anomalies.append(point)
        
        return anomalies


class MetricAlert:
    """Alert configuration and trigger"""
    
    def __init__(self, name: str, condition: Callable[[float], bool],
                 cooldown_seconds: int = 60):
        self.name = name
        self.condition = condition
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.last_alert: Optional[datetime] = None
    
    def should_alert(self, value: float) -> bool:
        """Check if alert should be triggered"""
        if not self.condition(value):
            return False
        
        if self.last_alert is None:
            self.last_alert = datetime.now()
            return True
        
        if datetime.now() - self.last_alert > self.cooldown:
            self.last_alert = datetime.now()
            return True
        
        return False


class MetricsCollector:
    """Central metrics collection system"""
    
    def __init__(self):
        self.metrics: Dict[str, TimeSeriesBuffer] = {}
        self.alerts: Dict[str, List[MetricAlert]] = {}
        self.lock = threading.RLock()
        self.anomaly_detectors: Dict[str, AnomalyDetector] = {}
    
    def register_metric(self, name: str, max_points: int = 10000) -> None:
        """Register new metric"""
        with self.lock:
            self.metrics[name] = TimeSeriesBuffer(max_points=max_points)
            self.anomaly_detectors[name] = AnomalyDetector()
    
    def record_metric(self, name: str, value: float, tags: Optional[Dict] = None) -> None:
        """Record metric value"""
        with self.lock:
            if name not in self.metrics:
                self.register_metric(name)
            
            self.metrics[name].add_point(value, tags)
            
            # Check alerts
            if name in self.alerts:
                for alert in self.alerts[name]:
                    if alert.should_alert(value):
                        self._trigger_alert(alert, value)
    
    def register_alert(self, metric_name: str, alert: MetricAlert) -> None:
        """Register alert for metric"""
        with self.lock:
            if metric_name not in self.alerts:
                self.alerts[metric_name] = []
            
            self.alerts[metric_name].append(alert)
    
    def _trigger_alert(self, alert: MetricAlert, value: float) -> None:
        """Trigger alert"""
        logger.warning(f"ALERT [{alert.name}]: value={value}")
    
    def get_metric_stats(self, name: str, seconds: int = 300) -> Dict[str, Any]:
        """Get metric statistics"""
        with self.lock:
            if name not in self.metrics:
                return {}
            
            return self.metrics[name].compute_stats(seconds)
    
    def detect_anomalies(self, name: str, seconds: int = 300) -> List[MetricPoint]:
        """Detect anomalies in metric"""
        with self.lock:
            if name not in self.metrics:
                return []
            
            detector = self.anomaly_detectors[name]
            return detector.detect(self.metrics[name], seconds)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for dashboard"""
        with self.lock:
            dashboard = {}
            
            for name in self.metrics:
                dashboard[name] = {
                    'stats': self.get_metric_stats(name),
                    'anomalies': len(self.detect_anomalies(name))
                }
            
            return dashboard


class MetricsReporter:
    """Generate metrics reports"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'alerts': {}
        }
        
        for name in self.collector.metrics:
            stats = self.collector.get_metric_stats(name)
            anomalies = self.collector.detect_anomalies(name)
            
            report['metrics'][name] = {
                'stats': stats,
                'anomaly_count': len(anomalies),
                'anomalies': [
                    {
                        'timestamp': a.timestamp.isoformat(),
                        'value': a.value
                    }
                    for a in anomalies[:10]  # Last 10 anomalies
                ]
            }
        
        return report


# Global instance
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector"""
    return _metrics_collector


def record_metric(name: str, value: float, tags: Optional[Dict] = None) -> None:
    """Convenience function to record metric"""
    _metrics_collector.record_metric(name, value, tags)

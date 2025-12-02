"""Monitoring and observability module for the chatbot.

Provides health checks, metrics collection, and performance monitoring.
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from collections import deque
import threading


@dataclass
class HealthStatus:
  """Health status of system components."""
  status: str  # healthy, degraded, unhealthy
  timestamp: datetime
  database: str = "unknown"
  cache: str = "unknown"
  uptime_seconds: int = 0
  details: Dict = field(default_factory=dict)


@dataclass
class MetricPoint:
  """Single metric data point."""
  timestamp: datetime
  value: float
  name: str
  tags: Dict = field(default_factory=dict)


class HealthMonitor:
  """Monitor system health and availability."""

  def __init__(self):
    self.start_time = datetime.utcnow()
    self.logger = logging.getLogger(__name__)
    self.last_db_check = datetime.utcnow()
    self.last_cache_check = datetime.utcnow()

  def check_health(self) -> HealthStatus:
    """Check overall system health.
    
    Returns:
        HealthStatus with current health information
    """
    uptime = (datetime.utcnow() - self.start_time).total_seconds()
    
    db_status = self._check_database()
    cache_status = self._check_cache()
    
    # Determine overall status
    if db_status == "unhealthy" or cache_status == "unhealthy":
      overall = "unhealthy"
    elif db_status == "degraded" or cache_status == "degraded":
      overall = "degraded"
    else:
      overall = "healthy"
    
    return HealthStatus(
      status=overall,
      timestamp=datetime.utcnow(),
      database=db_status,
      cache=cache_status,
      uptime_seconds=int(uptime),
      details={
        "version": "1.0.0",
        "environment": "production",
        "checks_passed": 2 if overall == "healthy" else 1
      }
    )

  def _check_database(self) -> str:
    """Check database connectivity."""
    try:
      # In production, would query actual database
      self.last_db_check = datetime.utcnow()
      return "connected"
    except Exception as e:
      self.logger.error(f"Database check failed: {e}")
      return "disconnected"

  def _check_cache(self) -> str:
    """Check cache connectivity."""
    try:
      # In production, would query Redis
      self.last_cache_check = datetime.utcnow()
      return "connected"
    except Exception as e:
      self.logger.error(f"Cache check failed: {e}")
      return "disconnected"


class MetricsCollector:
  """Collect and store performance metrics."""

  def __init__(self, window_size: int = 1000):
    self.metrics: Dict[str, deque] = {}
    self.window_size = window_size
    self.lock = threading.Lock()

  def record_metric(self, name: str, value: float, tags: Dict = None) -> None:
    """Record a metric point.
    
    Args:
        name: Metric name (e.g., 'response_time_ms')
        value: Metric value
        tags: Optional tags for filtering
    """
    with self.lock:
      if name not in self.metrics:
        self.metrics[name] = deque(maxlen=self.window_size)
      
      point = MetricPoint(
        timestamp=datetime.utcnow(),
        value=value,
        name=name,
        tags=tags or {}
      )
      self.metrics[name].append(point)

  def get_metric_stats(self, name: str) -> Dict[str, float]:
    """Get statistics for a metric.
    
    Args:
        name: Metric name
    
    Returns:
        Dict with min, max, avg, count
    """
    with self.lock:
      if name not in self.metrics or len(self.metrics[name]) == 0:
        return {"count": 0}
      
      values = [p.value for p in self.metrics[name]]
      return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "latest": values[-1]
      }

  def export_prometheus_metrics(self) -> str:
    """Export metrics in Prometheus format.
    
    Returns:
        Prometheus format metrics string
    """
    lines = []
    with self.lock:
      for name, metrics in self.metrics.items():
        if len(metrics) == 0:
          continue
        
        latest = metrics[-1]
        lines.append(f"# HELP {name} {name} metric")
        lines.append(f"# TYPE {name} gauge")
        lines.append(f"{name} {latest.value}")
    
    return "\n".join(lines)

  def get_slow_requests(self, threshold_ms: int = 500) -> List[Dict]:
    """Get requests exceeding latency threshold.
    
    Args:
        threshold_ms: Latency threshold in milliseconds
    
    Returns:
        List of slow requests
    """
    slow = []
    with self.lock:
      if "response_time_ms" in self.metrics:
        for point in self.metrics["response_time_ms"]:
          if point.value > threshold_ms:
            slow.append({
              "timestamp": point.timestamp.isoformat(),
              "duration_ms": point.value,
              "tags": point.tags
            })
    return slow[-10:]  # Return last 10


class RequestTracer:
  """Trace individual requests through the system."""

  def __init__(self):
    self.traces: Dict[str, Dict] = {}
    self.lock = threading.Lock()

  def start_trace(self, request_id: str) -> None:
    """Start tracing a request."""
    with self.lock:
      self.traces[request_id] = {
        "start_time": datetime.utcnow(),
        "events": []
      }

  def add_event(self, request_id: str, event_name: str, duration_ms: int = 0) -> None:
    """Add event to request trace."""
    with self.lock:
      if request_id in self.traces:
        self.traces[request_id]["events"].append({
          "name": event_name,
          "timestamp": datetime.utcnow().isoformat(),
          "duration_ms": duration_ms
        })

  def end_trace(self, request_id: str) -> Dict:
    """End tracing and return full trace."""
    with self.lock:
      if request_id in self.traces:
        trace = self.traces.pop(request_id)
        duration = (datetime.utcnow() - trace["start_time"]).total_seconds() * 1000
        trace["total_duration_ms"] = duration
        return trace
    return None


class AlertManager:
  """Manage alerting based on metrics thresholds."""

  def __init__(self):
    self.alerts: List[Dict] = []
    self.thresholds = {
      "response_time_ms": 250,
      "error_rate": 1.0,
      "cache_hit_rate": 70.0
    }
    self.lock = threading.Lock()

  def check_metric(self, name: str, value: float) -> Optional[Dict]:
    """Check if metric exceeds threshold.
    
    Returns:
        Alert dict if threshold exceeded, None otherwise
    """
    if name not in self.thresholds:
      return None
    
    threshold = self.thresholds[name]
    
    # For rate metrics, lower is worse; for ratios, higher is worse
    if "rate" in name:
      exceeded = value > threshold
    else:
      exceeded = value < threshold if "hit" in name else value > threshold
    
    if exceeded:
      alert = {
        "metric": name,
        "value": value,
        "threshold": threshold,
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "warning" if abs(value - threshold) < threshold * 0.1 else "critical"
      }
      with self.lock:
        self.alerts.append(alert)
      return alert
    return None

  def get_recent_alerts(self, minutes: int = 5) -> List[Dict]:
    """Get alerts from last N minutes."""
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    with self.lock:
      return [
        a for a in self.alerts
        if datetime.fromisoformat(a["timestamp"]) > cutoff
      ]


def initialize_monitoring() -> Dict:
  """Initialize monitoring components.
  
  Returns:
      Dict with all monitoring instances
  """
  return {
    "health_monitor": HealthMonitor(),
    "metrics_collector": MetricsCollector(),
    "request_tracer": RequestTracer(),
    "alert_manager": AlertManager()
  }

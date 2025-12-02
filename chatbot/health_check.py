"""Health check and monitoring endpoints for the chatbot system.

Provides:
- Health status endpoint for system monitoring
- Readiness checks for dependencies
- Performance metrics collection
- System diagnostics
"""

import time
import psutil
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class HealthStatus:
    """Health status data structure."""
    status: str  # healthy, degraded, unhealthy
    timestamp: str
    uptime_seconds: float
    checks: Dict[str, bool]
    metrics: Dict[str, Any]
    version: str = "1.0"


class HealthChecker:
    """System health monitoring and diagnostics."""

    def __init__(self, start_time: float = None):
        """Initialize health checker."""
        self.start_time = start_time or time.time()
        self.process = psutil.Process()

    def check_system_health(self) -> HealthStatus:
        """Perform comprehensive system health check."""
        checks = {
            'memory_available': self._check_memory(),
            'cpu_available': self._check_cpu(),
            'dependencies_loaded': self._check_dependencies(),
            'response_time_acceptable': self._check_response_time(),
        }

        metrics = self._collect_metrics()
        overall_status = 'healthy' if all(checks.values()) else 'degraded'

        return HealthStatus(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            uptime_seconds=time.time() - self.start_time,
            checks=checks,
            metrics=metrics,
        )

    def _check_memory(self) -> bool:
        """Check if system memory is available."""
        try:
            mem = psutil.virtual_memory()
            # Alert if memory usage > 90%
            return mem.percent < 90
        except Exception:
            return False

    def _check_cpu(self) -> bool:
        """Check if CPU availability is acceptable."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            # Alert if CPU usage > 80%
            return cpu_percent < 80
        except Exception:
            return False

    def _check_dependencies(self) -> bool:
        """Check if core dependencies are loaded."""
        try:
            # Verify core modules can be imported
            from chatbot.dialogue_system import DialogueSystem
            from chatbot.intent_classifier import IntentClassifier
            from chatbot.ir_based_qa import IRBasedQA
            return True
        except ImportError:
            return False

    def _check_response_time(self) -> bool:
        """Check if response times are acceptable."""
        try:
            from chatbot.dialogue_system import DialogueSystem
            start = time.time()
            ds = DialogueSystem()
            ds.process_input("Hello")
            elapsed = time.time() - start
            # Alert if response > 500ms
            return elapsed < 0.5
        except Exception:
            return False

    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics."""
        try:
            mem = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=0.1)
            process_mem = self.process.memory_info()

            return {
                'memory': {
                    'total_gb': mem.total / (1024**3),
                    'available_gb': mem.available / (1024**3),
                    'percent_used': mem.percent,
                },
                'cpu': {
                    'percent_used': cpu_percent,
                    'core_count': psutil.cpu_count(),
                },
                'process': {
                    'memory_mb': process_mem.rss / (1024**2),
                    'cpu_num': self.process.cpu_num(),
                },
            }
        except Exception as e:
            return {'error': str(e)}

    def get_readiness(self) -> Dict[str, Any]:
        """Check system readiness for requests."""
        health = self.check_system_health()
        return {
            'ready': health.status == 'healthy',
            'status': health.status,
            'timestamp': health.timestamp,
            'checks': health.checks,
        }


class MetricsCollector:
    """Collect and aggregate chatbot metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0
        self.intent_distribution = {}
        self.start_time = time.time()

    def record_request(self, intent: str, response_time: float, error: bool = False):
        """Record a processed request."""
        self.request_count += 1
        self.total_response_time += response_time
        if error:
            self.error_count += 1
        self.intent_distribution[intent] = self.intent_distribution.get(intent, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics."""
        uptime = time.time() - self.start_time
        avg_response_time = (self.total_response_time / self.request_count * 1000 
                            if self.request_count > 0 else 0)

        return {
            'uptime_seconds': uptime,
            'total_requests': self.request_count,
            'error_count': self.error_count,
            'error_rate': (self.error_count / self.request_count 
                          if self.request_count > 0 else 0),
            'avg_response_time_ms': avg_response_time,
            'requests_per_second': (self.request_count / uptime if uptime > 0 else 0),
            'intent_distribution': self.intent_distribution,
        }


if __name__ == '__main__':
    checker = HealthChecker()
    health = checker.check_system_health()
    print(f"Health Status: {health.status}")
    print(f"Checks: {health.checks}")
    print(f"Metrics: {health.metrics}")

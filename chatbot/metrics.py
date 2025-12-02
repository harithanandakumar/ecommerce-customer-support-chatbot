"""Performance metrics collection and aggregation."""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
import threading
from statistics import mean, median, stdev


@dataclass
class MetricsAggregator:
  """Aggregate and compute metrics statistics."""
  
  def __init__(self):
    self.response_times: List[float] = []
    self.error_counts: Dict[str, int] = {}
    self.operation_counts: Dict[str, int] = {}
    self.lock = threading.Lock()

  def record_response_time(self, endpoint: str, duration_ms: float) -> None:
    """Record response time for endpoint."""
    with self.lock:
      self.response_times.append(duration_ms)
      if endpoint not in self.operation_counts:
        self.operation_counts[endpoint] = 0
      self.operation_counts[endpoint] += 1

  def record_error(self, error_type: str) -> None:
    """Record error occurrence."""
    with self.lock:
      if error_type not in self.error_counts:
        self.error_counts[error_type] = 0
      self.error_counts[error_type] += 1

  def get_response_time_stats(self) -> Dict:
    """Get response time statistics."""
    with self.lock:
      if not self.response_times:
        return {"count": 0}
      
      times = sorted(self.response_times)
      return {
        "count": len(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "avg_ms": mean(times),
        "median_ms": median(times),
        "p95_ms": times[int(len(times) * 0.95)],
        "p99_ms": times[int(len(times) * 0.99)],
        "stdev": stdev(times) if len(times) > 1 else 0
      }

  def get_error_stats(self) -> Dict:
    """Get error statistics."""
    with self.lock:
      total = sum(self.error_counts.values())
      return {
        "total": total,
        "by_type": dict(self.error_counts)
      }

  def get_throughput_stats(self) -> Dict:
    """Get throughput statistics."""
    with self.lock:
      return dict(self.operation_counts)

  def reset(self) -> None:
    """Reset all metrics."""
    with self.lock:
      self.response_times.clear()
      self.error_counts.clear()
      self.operation_counts.clear()


class IntentMetrics:
  """Track intent classification metrics."""
  
  def __init__(self):
    self.classifications: Dict[str, int] = {}
    self.accuracy_total: int = 0
    self.accuracy_correct: int = 0
    self.lock = threading.Lock()

  def record_classification(self, intent: str, correct: bool) -> None:
    """Record intent classification result."""
    with self.lock:
      if intent not in self.classifications:
        self.classifications[intent] = 0
      self.classifications[intent] += 1
      self.accuracy_total += 1
      if correct:
        self.accuracy_correct += 1

  def get_accuracy(self) -> float:
    """Get overall classification accuracy."""
    with self.lock:
      if self.accuracy_total == 0:
        return 0.0
      return (self.accuracy_correct / self.accuracy_total) * 100

  def get_intent_distribution(self) -> Dict[str, float]:
    """Get intent distribution percentages."""
    with self.lock:
      total = sum(self.classifications.values())
      if total == 0:
        return {}
      return {
        intent: (count / total) * 100
        for intent, count in self.classifications.items()
      }


class OrderMetrics:
  """Track order operation metrics."""
  
  def __init__(self):
    self.tracking_total: int = 0
    self.tracking_success: int = 0
    self.cancellation_total: int = 0
    self.cancellation_success: int = 0
    self.lock = threading.Lock()

  def record_tracking(self, success: bool) -> None:
    """Record order tracking operation."""
    with self.lock:
      self.tracking_total += 1
      if success:
        self.tracking_success += 1

  def record_cancellation(self, success: bool) -> None:
    """Record order cancellation operation."""
    with self.lock:
      self.cancellation_total += 1
      if success:
        self.cancellation_success += 1

  def get_success_rates(self) -> Dict[str, float]:
    """Get success rates for operations."""
    with self.lock:
      tracking_rate = 0.0
      if self.tracking_total > 0:
        tracking_rate = (self.tracking_success / self.tracking_total) * 100
      
      cancellation_rate = 0.0
      if self.cancellation_total > 0:
        cancellation_rate = (self.cancellation_success / self.cancellation_total) * 100
      
      return {
        "tracking_success_rate": tracking_rate,
        "cancellation_success_rate": cancellation_rate,
        "overall_success_rate": ((self.tracking_success + self.cancellation_success) / 
                                  (self.tracking_total + self.cancellation_total) * 100)
                                if (self.tracking_total + self.cancellation_total) > 0 else 0.0
      }


class CacheMetrics:
  """Track cache performance."""
  
  def __init__(self):
    self.hits: int = 0
    self.misses: int = 0
    self.evictions: int = 0
    self.lock = threading.Lock()

  def record_hit(self) -> None:
    """Record cache hit."""
    with self.lock:
      self.hits += 1

  def record_miss(self) -> None:
    """Record cache miss."""
    with self.lock:
      self.misses += 1

  def record_eviction(self) -> None:
    """Record cache eviction."""
    with self.lock:
      self.evictions += 1

  def get_hit_rate(self) -> float:
    """Get cache hit rate percentage."""
    with self.lock:
      total = self.hits + self.misses
      if total == 0:
        return 0.0
      return (self.hits / total) * 100

  def get_stats(self) -> Dict:
    """Get cache statistics."""
    with self.lock:
      total = self.hits + self.misses
      return {
        "hits": self.hits,
        "misses": self.misses,
        "evictions": self.evictions,
        "hit_rate_percent": (self.hits / total * 100) if total > 0 else 0,
        "total_accesses": total
      }


def initialize_metrics() -> Dict:
  """Initialize all metrics collectors."""
  return {
    "aggregator": MetricsAggregator(),
    "intent": IntentMetrics(),
    "order": OrderMetrics(),
    "cache": CacheMetrics()
  }

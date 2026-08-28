"""
VULTURE Performance Optimizer Module
=====================================
Advanced optimization system with intelligent caching, parallel processing,
and performance profiling for maximum efficiency.

Features:
    - Multi-level caching (LRU, TTL)
    - Parallel task execution
    - Memory optimization
    - Performance profiling
    - Bottleneck detection
    - Auto-scaling
"""

import functools
import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import OrderedDict
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class CacheStats:
    """Cache statistics tracker"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    memory_used: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


class LRUCache:
    """Thread-safe LRU Cache with TTL support"""
    
    def __init__(self, max_size: int = 128, ttl_seconds: Optional[int] = None):
        self.max_size = max_size
        self.ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else None
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict = {}
        self.lock = threading.RLock()
        self.stats = CacheStats()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key not in self.cache:
                self.stats.misses += 1
                return None
            
            # Check TTL
            if self.ttl and key in self.timestamps:
                if datetime.now() - self.timestamps[key] > self.ttl:
                    del self.cache[key]
                    del self.timestamps[key]
                    self.stats.misses += 1
                    return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.stats.hits += 1
            return self.cache[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
            
            # Evict oldest if over capacity
            if len(self.cache) > self.max_size:
                oldest_key, _ = self.cache.popitem(last=False)
                del self.timestamps[oldest_key]
                self.stats.evictions += 1
    
    def clear(self) -> None:
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        return self.stats


class ParallelExecutor:
    """Parallel task executor with adaptive thread pool"""
    
    def __init__(self, max_workers: Optional[int] = None, use_processes: bool = False):
        if max_workers is None:
            max_workers = max(1, psutil.cpu_count(logical=False))
        
        self.max_workers = max_workers
        self.use_processes = use_processes
        self.executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
        self.executor = self.executor_class(max_workers=max_workers)
    
    def map(self, func: Callable, iterable: List) -> List[Any]:
        """Map function across iterable in parallel"""
        try:
            return list(self.executor.map(func, iterable, timeout=300))
        except Exception as e:
            logger.error(f"Parallel execution error: {e}")
            return [func(item) for item in iterable]
    
    def submit_batch(self, tasks: List[Tuple[Callable, tuple]]) -> List[Any]:
        """Submit batch of tasks and wait for completion"""
        futures = []
        for func, args in tasks:
            futures.append(self.executor.submit(func, *args))
        
        results = []
        for future in futures:
            try:
                results.append(future.result(timeout=300))
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                results.append(None)
        
        return results
    
    def shutdown(self) -> None:
        """Shutdown executor"""
        self.executor.shutdown(wait=True)


class PerformanceProfiler:
    """Performance profiling and bottleneck detection"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.lock = threading.Lock()
    
    def profile(self, name: str) -> Any:
        """Decorator for profiling function execution"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.perf_counter()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.perf_counter()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    
                    duration = end_time - start_time
                    memory_delta = end_memory - start_memory
                    
                    with self.lock:
                        if name not in self.metrics:
                            self.metrics[name] = []
                        self.metrics[name].append(duration)
                    
                    logger.debug(
                        f"{name}: {duration:.4f}s, Memory: {memory_delta:+.2f}MB"
                    )
            return wrapper
        return decorator
    
    def get_report(self) -> Dict[str, Dict[str, float]]:
        """Get performance report"""
        report = {}
        with self.lock:
            for name, times in self.metrics.items():
                if times:
                    report[name] = {
                        'avg': sum(times) / len(times),
                        'min': min(times),
                        'max': max(times),
                        'calls': len(times)
                    }
        return report
    
    def find_bottlenecks(self, threshold_ms: float = 100) -> List[str]:
        """Identify functions exceeding threshold"""
        bottlenecks = []
        report = self.get_report()
        
        for name, stats in report.items():
            if stats['avg'] * 1000 > threshold_ms:
                bottlenecks.append(name)
        
        return bottlenecks


class MemoryOptimizer:
    """Memory usage optimization"""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get detailed memory usage"""
        process = psutil.Process()
        return {
            'rss': process.memory_info().rss / 1024 / 1024,  # MB
            'vms': process.memory_info().vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    @staticmethod
    def optimize_array(array) -> Any:
        """Optimize numpy array memory usage"""
        try:
            import numpy as np
            if not isinstance(array, np.ndarray):
                return array
            
            # Use most memory-efficient dtype
            if array.dtype == np.float64:
                return array.astype(np.float32)
            elif array.dtype == np.int64:
                if array.max() < 2**31:
                    return array.astype(np.int32)
            
            return array
        except Exception as e:
            logger.warning(f"Array optimization failed: {e}")
            return array
    
    @staticmethod
    def clear_memory() -> None:
        """Force garbage collection"""
        import gc
        gc.collect()


class PerformanceManager:
    """Central performance management"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
        
        self.cache = LRUCache(max_size=256, ttl_seconds=3600)
        self.executor = ParallelExecutor(max_workers=4)
        self.profiler = PerformanceProfiler()
        self.memory_optimizer = MemoryOptimizer()
        self.initialized = True
    
    def get_cache(self) -> LRUCache:
        """Get cache instance"""
        return self.cache
    
    def get_executor(self) -> ParallelExecutor:
        """Get executor instance"""
        return self.executor
    
    def get_profiler(self) -> PerformanceProfiler:
        """Get profiler instance"""
        return self.profiler
    
    def get_memory_optimizer(self) -> MemoryOptimizer:
        """Get memory optimizer instance"""
        return self.memory_optimizer
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            'cache': {
                'hits': self.cache.stats.hits,
                'misses': self.cache.stats.misses,
                'hit_rate': f"{self.cache.stats.hit_rate:.2f}%"
            },
            'profiling': self.profiler.get_report(),
            'bottlenecks': self.profiler.find_bottlenecks(),
            'memory': self.memory_optimizer.get_memory_usage(),
            'timestamp': datetime.now().isoformat()
        }
    
    def shutdown(self) -> None:
        """Shutdown all services"""
        self.executor.shutdown()
        self.cache.clear()


# Global instance
_performance_manager = PerformanceManager()


def get_performance_manager() -> PerformanceManager:
    """Get global performance manager"""
    return _performance_manager

"""
Memory monitoring utilities for the JobQueueProcessor
"""
import gc
import logging
import psutil
import threading
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class MemoryMonitor:
    """Memory monitoring and management utility"""
    
    def __init__(self, alert_threshold: float = 80.0, cleanup_threshold: float = 70.0):
        self.alert_threshold = alert_threshold  # Alert when memory usage exceeds this %
        self.cleanup_threshold = cleanup_threshold  # Force cleanup when memory usage exceeds this %
        self.monitoring = False
        self.monitor_thread = None
        self.cleanup_callbacks = []
        
    def add_cleanup_callback(self, callback):
        """Add a callback function to be called during memory cleanup"""
        self.cleanup_callbacks.append(callback)
    
    def start_monitoring(self, interval: int = 30):
        """Start memory monitoring in a separate thread"""
        if self.monitoring:
            logger.warning("Memory monitoring is already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval,), 
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Memory monitoring started (interval: {interval}s, alert: {self.alert_threshold}%, cleanup: {self.cleanup_threshold}%)")
    
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Memory monitoring stopped")
    
    def _monitor_loop(self, interval: int):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                memory_info = self.get_memory_info()
                memory_percent = memory_info['percent']
                
                if memory_percent >= self.alert_threshold:
                    logger.warning(f"🚨 HIGH MEMORY USAGE: {memory_percent:.1f}% (threshold: {self.alert_threshold}%)")
                    
                    if memory_percent >= self.cleanup_threshold:
                        logger.warning(f"🧹 FORCING MEMORY CLEANUP: {memory_percent:.1f}% (threshold: {self.cleanup_threshold}%)")
                        self.force_cleanup()
                
                elif memory_percent >= 60:
                    logger.info(f"📊 Moderate memory usage: {memory_percent:.1f}%")
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in memory monitoring: {str(e)}")
                time.sleep(interval)
    
    def get_memory_info(self) -> Dict:
        """Get current memory usage information"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': process.memory_percent(),
                'available_mb': psutil.virtual_memory().available / 1024 / 1024,
                'total_mb': psutil.virtual_memory().total / 1024 / 1024,
                'pid': process.pid
            }
        except Exception as e:
            logger.error(f"Error getting memory info: {str(e)}")
            return {
                'rss_mb': 0,
                'vms_mb': 0,
                'percent': 0,
                'available_mb': 0,
                'total_mb': 0,
                'pid': 0
            }
    
    def force_cleanup(self):
        """Force memory cleanup by running garbage collection and callbacks"""
        try:
            logger.info("🧹 Starting forced memory cleanup...")
            
            # Run garbage collection
            collected = gc.collect()
            logger.info(f"🗑️ Garbage collection completed, collected {collected} objects")
            
            # Run cleanup callbacks
            for callback in self.cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error in cleanup callback: {str(e)}")
            
            # Log memory after cleanup
            memory_info = self.get_memory_info()
            logger.info(f"✅ Memory cleanup completed - Current usage: {memory_info['percent']:.1f}% ({memory_info['rss_mb']:.1f}MB)")
            
        except Exception as e:
            logger.error(f"Error during forced cleanup: {str(e)}")
    
    def log_memory_usage(self, context: str = ""):
        """Log current memory usage"""
        memory_info = self.get_memory_info()
        logger.info(f"🧠 Memory usage {context}: {memory_info['rss_mb']:.1f}MB ({memory_info['percent']:.1f}%) - Available: {memory_info['available_mb']:.1f}MB")


# Global memory monitor instance
_memory_monitor: Optional[MemoryMonitor] = None


def get_memory_monitor() -> MemoryMonitor:
    """Get the global memory monitor instance"""
    global _memory_monitor
    if _memory_monitor is None:
        _memory_monitor = MemoryMonitor()
    return _memory_monitor


def start_memory_monitoring(interval: int = 30):
    """Start global memory monitoring"""
    monitor = get_memory_monitor()
    monitor.start_monitoring(interval)


def stop_memory_monitoring():
    """Stop global memory monitoring"""
    global _memory_monitor
    if _memory_monitor:
        _memory_monitor.stop_monitoring()
        _memory_monitor = None


def log_memory_usage(context: str = ""):
    """Log current memory usage using global monitor"""
    monitor = get_memory_monitor()
    monitor.log_memory_usage(context)

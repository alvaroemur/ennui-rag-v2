#!/usr/bin/env python3
"""
Memory Leak Detection and Monitoring Script for JobQueueProcessor

This script helps identify and monitor memory leaks in the JobQueueProcessor.
Run this script alongside the processor to get detailed memory usage reports.
"""

import argparse
import gc
import logging
import psutil
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
from memory_monitor import MemoryMonitor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MemoryLeakDetector:
    """Advanced memory leak detection and analysis"""
    
    def __init__(self, process_name: str = "python", check_interval: int = 10):
        self.process_name = process_name
        self.check_interval = check_interval
        self.monitoring = False
        self.memory_history: List[Dict] = []
        self.leak_threshold_mb = 50  # Alert if memory increases by this much
        self.leak_threshold_percent = 20  # Alert if memory increases by this percentage
        
    def find_target_process(self) -> Optional[psutil.Process]:
        """Find the target process by name"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if self.process_name in proc.info['name'] or any(self.process_name in arg for arg in proc.info['cmdline']):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def get_process_memory_info(self, proc: psutil.Process) -> Dict:
        """Get detailed memory information for a process"""
        try:
            memory_info = proc.memory_info()
            memory_percent = proc.memory_percent()
            
            return {
                'timestamp': datetime.now(),
                'pid': proc.pid,
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': memory_percent,
                'num_threads': proc.num_threads(),
                'num_fds': proc.num_fds() if hasattr(proc, 'num_fds') else 0,
                'cpu_percent': proc.cpu_percent(),
                'status': proc.status()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.error(f"Error getting process info: {e}")
            return {}
    
    def detect_memory_leak(self, current: Dict, previous: Dict) -> Optional[str]:
        """Detect potential memory leaks based on memory growth patterns"""
        if not previous:
            return None
        
        rss_growth = current['rss_mb'] - previous['rss_mb']
        percent_growth = ((current['rss_mb'] - previous['rss_mb']) / previous['rss_mb']) * 100
        
        # Check for significant memory growth
        if rss_growth > self.leak_threshold_mb:
            return f"🚨 LARGE MEMORY GROWTH: +{rss_growth:.1f}MB in {self.check_interval}s"
        
        if percent_growth > self.leak_threshold_percent:
            return f"⚠️ HIGH MEMORY GROWTH: +{percent_growth:.1f}% in {self.check_interval}s"
        
        # Check for consistent growth over multiple intervals
        if len(self.memory_history) >= 5:
            recent_growth = sum(
                self.memory_history[i]['rss_mb'] - self.memory_history[i-1]['rss_mb'] 
                for i in range(-4, 0)
            )
            if recent_growth > self.leak_threshold_mb * 2:
                return f"📈 CONSISTENT GROWTH: +{recent_growth:.1f}MB over last 5 intervals"
        
        return None
    
    def analyze_memory_patterns(self):
        """Analyze memory usage patterns for leak detection"""
        if len(self.memory_history) < 10:
            return
        
        # Calculate growth rate
        start_memory = self.memory_history[0]['rss_mb']
        end_memory = self.memory_history[-1]['rss_mb']
        total_growth = end_memory - start_memory
        time_span = (self.memory_history[-1]['timestamp'] - self.memory_history[0]['timestamp']).total_seconds()
        growth_rate = total_growth / (time_span / 60) if time_span > 0 else 0  # MB per minute
        
        logger.info(f"📊 Memory Analysis:")
        logger.info(f"   Start: {start_memory:.1f}MB")
        logger.info(f"   Current: {end_memory:.1f}MB")
        logger.info(f"   Total Growth: {total_growth:.1f}MB")
        logger.info(f"   Growth Rate: {growth_rate:.2f}MB/min")
        
        if growth_rate > 5:  # More than 5MB per minute
            logger.warning(f"🚨 POTENTIAL MEMORY LEAK: High growth rate of {growth_rate:.2f}MB/min")
        
        # Check for memory spikes
        memory_values = [entry['rss_mb'] for entry in self.memory_history]
        max_memory = max(memory_values)
        min_memory = min(memory_values)
        memory_variance = max_memory - min_memory
        
        if memory_variance > 100:  # More than 100MB variance
            logger.warning(f"📈 HIGH MEMORY VARIANCE: {memory_variance:.1f}MB (min: {min_memory:.1f}MB, max: {max_memory:.1f}MB)")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        target_proc = None
        
        while self.monitoring:
            try:
                # Find target process if not found or if it died
                if target_proc is None:
                    target_proc = self.find_target_process()
                    if target_proc is None:
                        logger.warning(f"Target process '{self.process_name}' not found, retrying...")
                        time.sleep(self.check_interval)
                        continue
                    else:
                        logger.info(f"Found target process: PID {target_proc.pid}")
                
                # Get memory info
                memory_info = self.get_process_memory_info(target_proc)
                if not memory_info:
                    target_proc = None
                    continue
                
                # Store in history
                self.memory_history.append(memory_info)
                
                # Keep only last 100 entries
                if len(self.memory_history) > 100:
                    self.memory_history = self.memory_history[-100:]
                
                # Check for memory leaks
                previous = self.memory_history[-2] if len(self.memory_history) > 1 else None
                leak_warning = self.detect_memory_leak(memory_info, previous)
                
                if leak_warning:
                    logger.warning(leak_warning)
                
                # Log current status
                logger.info(f"🧠 Process {memory_info['pid']}: {memory_info['rss_mb']:.1f}MB ({memory_info['percent']:.1f}%) - "
                           f"Threads: {memory_info['num_threads']}, FDs: {memory_info['num_fds']}")
                
                # Analyze patterns every 10 intervals
                if len(self.memory_history) % 10 == 0:
                    self.analyze_memory_patterns()
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """Start memory leak monitoring"""
        if self.monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.monitoring = True
        logger.info(f"Starting memory leak detection for process '{self.process_name}' (interval: {self.check_interval}s)")
        
        try:
            self.monitor_loop()
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        finally:
            self.monitoring = False
            self.analyze_memory_patterns()
    
    def generate_report(self):
        """Generate a detailed memory usage report"""
        if not self.memory_history:
            logger.warning("No memory data available for report")
            return
        
        logger.info("=" * 60)
        logger.info("MEMORY LEAK DETECTION REPORT")
        logger.info("=" * 60)
        
        # Basic stats
        memory_values = [entry['rss_mb'] for entry in self.memory_history]
        start_memory = memory_values[0]
        end_memory = memory_values[-1]
        max_memory = max(memory_values)
        min_memory = min(memory_values)
        
        logger.info(f"Monitoring Duration: {len(self.memory_history)} intervals")
        logger.info(f"Start Memory: {start_memory:.1f}MB")
        logger.info(f"End Memory: {end_memory:.1f}MB")
        logger.info(f"Peak Memory: {max_memory:.1f}MB")
        logger.info(f"Min Memory: {min_memory:.1f}MB")
        logger.info(f"Total Growth: {end_memory - start_memory:.1f}MB")
        logger.info(f"Memory Variance: {max_memory - min_memory:.1f}MB")
        
        # Growth analysis
        if len(memory_values) > 1:
            growth_rate = (end_memory - start_memory) / len(memory_values)
            logger.info(f"Average Growth per Interval: {growth_rate:.2f}MB")
            
            if growth_rate > 1:
                logger.warning(f"🚨 CONSISTENT MEMORY GROWTH: {growth_rate:.2f}MB per interval")
        
        logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Memory Leak Detector for JobQueueProcessor")
    parser.add_argument("--process", default="python", help="Process name to monitor")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    parser.add_argument("--threshold-mb", type=float, default=50, help="Memory growth threshold in MB")
    parser.add_argument("--threshold-percent", type=float, default=20, help="Memory growth threshold in percent")
    
    args = parser.parse_args()
    
    detector = MemoryLeakDetector(
        process_name=args.process,
        check_interval=args.interval
    )
    detector.leak_threshold_mb = args.threshold_mb
    detector.leak_threshold_percent = args.threshold_percent
    
    try:
        detector.start_monitoring()
    finally:
        detector.generate_report()


if __name__ == "__main__":
    main()

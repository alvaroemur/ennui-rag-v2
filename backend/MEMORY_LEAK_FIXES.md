# Memory Leak Fixes for JobQueueProcessor

## Overview

This document outlines the comprehensive memory leak fixes implemented in the JobQueueProcessor to address memory accumulation issues during file processing.

## Memory Leak Issues Identified and Fixed

### 1. Event Loop Memory Leaks
**Problem**: Creating new asyncio event loops in `_scan_folder_sync()` and `_process_file_sync()` without proper cleanup.

**Solution**: 
- Replaced `asyncio.new_event_loop()` with `asyncio.run()`
- Proper cleanup of event loops to prevent memory accumulation
- Added error handling for event loop creation

### 2. Large File Content Memory Issues
**Problem**: Storing entire file contents in memory without size limits, causing memory spikes.

**Solution**:
- Added file size limits (50MB default) before processing
- Implemented streaming downloads for large files using 8KB chunks
- Immediate cleanup of `content_bytes` after processing
- Added file size logging for monitoring

### 3. Database Session Management
**Problem**: Multiple database sessions not properly closed, leading to connection leaks.

**Solution**:
- Improved database session cleanup in all methods
- Added proper exception handling with rollback
- Ensured sessions are closed in finally blocks

### 4. Missing Garbage Collection
**Problem**: No explicit garbage collection, allowing memory to accumulate.

**Solution**:
- Added periodic garbage collection every 100 files processed
- Force garbage collection after each job completion
- Added memory cleanup callbacks

### 5. Memory Monitoring and Alerting
**Problem**: No visibility into memory usage patterns during processing.

**Solution**:
- Created comprehensive memory monitoring system
- Added memory usage logging at key points
- Implemented memory leak detection with thresholds
- Added process monitoring capabilities

## New Features Added

### Memory Monitor (`memory_monitor.py`)
- Real-time memory usage tracking
- Configurable alert thresholds (default: 80% warning, 70% cleanup)
- Automatic memory cleanup when thresholds are exceeded
- Memory usage logging with context

### Memory Leak Detector (`memory_leak_detector.py`)
- Standalone script for monitoring memory leaks
- Process-specific monitoring
- Growth rate analysis
- Detailed memory usage reports
- Pattern detection for consistent memory growth

### Enhanced JobQueueProcessor
- Memory management settings (max file size, cleanup intervals)
- Comprehensive memory logging throughout processing
- File size validation before processing
- Periodic memory cleanup
- Memory monitoring integration

## Configuration Options

### JobQueueProcessor Memory Settings
```python
# In JobQueueProcessor.__init__()
self.max_file_size_mb = 50  # Maximum file size to process (MB)
self.memory_cleanup_interval = 100  # Cleanup memory every N files
```

### Memory Monitor Settings
```python
# In MemoryMonitor.__init__()
self.alert_threshold = 80.0  # Alert when memory usage exceeds this %
self.cleanup_threshold = 70.0  # Force cleanup when memory usage exceeds this %
```

## Usage

### Running with Memory Monitoring
```python
from apps.job_queue_processor import JobQueueProcessor

# Create processor with memory management
processor = JobQueueProcessor()
processor.start()  # Automatically starts memory monitoring
```

### Using Memory Leak Detector
```bash
# Monitor the JobQueueProcessor process
python memory_leak_detector.py --process python --interval 10

# Monitor with custom thresholds
python memory_leak_detector.py --process python --threshold-mb 100 --threshold-percent 25
```

### Manual Memory Monitoring
```python
from memory_monitor import log_memory_usage, get_memory_monitor

# Log current memory usage
log_memory_usage("Before processing large file")

# Get detailed memory info
monitor = get_memory_monitor()
memory_info = monitor.get_memory_info()
print(f"Memory: {memory_info['rss_mb']:.1f}MB ({memory_info['percent']:.1f}%)")
```

## Memory Usage Logging

The enhanced processor now logs memory usage at key points:

- **Processor initialization**: Initial memory state
- **Job start/end**: Memory before and after each job
- **File processing**: Memory before and after each file
- **Progress checkpoints**: Every 10 files processed
- **Memory cleanup**: Before and after garbage collection
- **Error conditions**: Memory state when errors occur

### Log Format
```
🧠 Memory usage [context]: 123.4MB (45.2%) - Available: 1024.0MB
```

## Performance Improvements

### File Processing Optimizations
- **Streaming downloads**: Large files are downloaded in 8KB chunks
- **Size limits**: Files larger than 50MB are skipped with warning
- **Immediate cleanup**: Memory is freed as soon as content is processed
- **Chunked processing**: Content is processed in manageable chunks

### Memory Management
- **Periodic cleanup**: Garbage collection every 100 files
- **Force cleanup**: After each job completion
- **Threshold-based cleanup**: Automatic cleanup when memory usage is high
- **Process monitoring**: Real-time memory usage tracking

## Monitoring and Debugging

### Memory Leak Detection
The memory leak detector can identify:
- Large memory growth spikes (>50MB in 10 seconds)
- High percentage growth (>20% in 10 seconds)
- Consistent memory growth over time
- Memory variance patterns

### Log Analysis
Look for these log patterns to identify issues:
- `🚨 HIGH MEMORY USAGE`: Memory usage exceeds 80%
- `⚠️ Skipping large file`: Files being skipped due to size limits
- `🧹 Running memory cleanup`: Automatic cleanup being triggered
- `📈 CONSISTENT GROWTH`: Potential memory leak detected

## Dependencies Added

- `psutil==5.9.0`: Process and system monitoring
- `gc`: Built-in garbage collection (already available)

## Testing Memory Leak Fixes

### 1. Run Memory Leak Detector
```bash
cd backend
python memory_leak_detector.py --process python --interval 5
```

### 2. Process Large Files
Create indexing jobs with large files to test size limits and memory management.

### 3. Monitor Logs
Watch for memory usage logs and cleanup messages during processing.

### 4. Check Memory Growth
Use the memory leak detector to verify that memory growth is controlled and doesn't exceed thresholds.

## Troubleshooting

### High Memory Usage
1. Check if large files are being processed (look for size warnings)
2. Verify memory cleanup is running (look for cleanup logs)
3. Check if file size limits are appropriate for your use case
4. Monitor memory growth patterns with the leak detector

### Memory Leaks Still Occurring
1. Run the memory leak detector to identify growth patterns
2. Check logs for specific files causing issues
3. Adjust file size limits if needed
4. Verify garbage collection is running properly

### Performance Issues
1. Adjust memory cleanup intervals
2. Tune file size limits
3. Monitor memory thresholds
4. Check for excessive logging (reduce log level if needed)

## Future Improvements

1. **Configurable thresholds**: Make memory limits configurable via environment variables
2. **Memory profiling**: Add detailed memory profiling for specific operations
3. **Database connection pooling**: Implement connection pooling for better resource management
4. **Async processing**: Consider converting more operations to async for better memory efficiency
5. **Memory compression**: Implement content compression for large text files

## Conclusion

These fixes address the major memory leak sources in the JobQueueProcessor:
- Event loop leaks are eliminated
- Large file processing is controlled
- Memory cleanup is automated
- Monitoring provides visibility into memory usage
- Database connections are properly managed

The processor should now maintain stable memory usage even during intensive file processing operations.

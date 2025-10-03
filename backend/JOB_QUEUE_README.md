# Job Queue System

This document describes the new database-based job queue system that replaces the previous BackgroundTasks and asyncio implementation.

## Overview

The job queue system processes indexing jobs sequentially using a database table as the queue. This provides better reliability, persistence, and monitoring capabilities compared to the previous in-memory background task system.

## Architecture

### Components

1. **IndexingJob Model** - Extended database model that serves as the job queue
2. **JobQueueProcessor** - Background service that processes jobs from the queue
3. **IndexingService** - Updated to create jobs in the queue instead of using BackgroundTasks
4. **API Endpoints** - New endpoints for managing the job queue

### Key Features

- **Sequential Processing**: Jobs are processed one at a time to avoid resource conflicts
- **Priority Support**: Jobs can have different priority levels
- **Retry Logic**: Failed jobs are automatically retried with exponential backoff
- **Job Locking**: Prevents multiple processors from working on the same job
- **Persistence**: Jobs survive server restarts
- **Monitoring**: Full visibility into job status and queue statistics

## Database Schema

The `IndexingJob` table has been extended with the following fields:

```sql
-- Queue management
priority INTEGER DEFAULT 0,           -- Higher number = higher priority
retry_count INTEGER DEFAULT 0,        -- Number of retry attempts
max_retries INTEGER DEFAULT 3,        -- Maximum retry attempts
scheduled_at TIMESTAMP WITH TIME ZONE, -- When to process the job
locked_at TIMESTAMP WITH TIME ZONE,   -- When job was locked for processing
locked_by VARCHAR,                    -- Process identifier that locked the job

-- Job parameters (stored as JSON)
job_parameters TEXT,                  -- JSON string with job-specific parameters
```

## Usage

### Starting the Job Processor

The job processor can be started in several ways:

#### 1. Automatically with API (Recommended)
The job processor starts automatically when the API starts:

```bash
python -m uvicorn apps.api:api_app --host 0.0.0.0 --port 8000
```

#### 2. Standalone Processor
Run a dedicated job processor:

```bash
python run_job_processor.py --daemon
```

#### 3. Multiple Processors
Run multiple processors for higher throughput:

```bash
python run_job_processor.py --process-id processor-1 --daemon
python run_job_processor.py --process-id processor-2 --daemon
```

### Creating Jobs

Jobs are created using the updated `IndexingService`:

```python
from apps.indexing_service import IndexingService

# Create a job
indexing_service = IndexingService(db)
job = indexing_service.create_indexing_job(
    program_id=1,
    user_id=1,
    folder_id="folder_123",
    job_type="specific_folder",
    priority=1,  # Higher priority
    access_token="google_token",
    include_trashed=False
)
```

### API Endpoints

#### Get Queue Status
```http
GET /job-queue/status
```

Returns:
```json
{
  "queue": {
    "pending_jobs": 5,
    "running_jobs": 1,
    "completed_jobs": 100,
    "failed_jobs": 3,
    "oldest_pending_job": {
      "id": 123,
      "created_at": "2024-01-01T10:00:00Z",
      "job_type": "full_scan"
    }
  },
  "processor": {
    "process_id": "processor_abc123",
    "running": true,
    "thread_alive": true,
    "shutdown_requested": false
  },
  "is_processor_running": true
}
```

#### Get Program Jobs
```http
GET /job-queue/jobs/{program_id}?limit=20
```

#### Cancel Job
```http
POST /job-queue/jobs/{job_id}/cancel
```

#### Start/Stop Processor
```http
POST /job-queue/start-processor
POST /job-queue/stop-processor
```

## Migration

To migrate from the old system to the new job queue system:

1. **Run Database Migration**:
   ```bash
   python migrate_job_queue.py
   ```

2. **Update Code**: The API endpoints have been updated to use the new system automatically.

3. **Start Job Processor**: The processor starts automatically with the API.

## Job Processing Flow

1. **Job Creation**: Jobs are created and added to the queue with status "pending"
2. **Job Selection**: The processor selects the next job based on priority and creation time
3. **Job Locking**: The selected job is locked to prevent other processors from taking it
4. **Job Processing**: The job is processed synchronously
5. **Job Completion**: The job status is updated to "completed" or "failed"
6. **Retry Logic**: Failed jobs are retried up to `max_retries` times

## Error Handling

- **Job Failures**: Jobs that fail are automatically retried with exponential backoff
- **Processor Crashes**: Jobs locked by crashed processors are automatically unlocked after a timeout
- **Database Errors**: Database connection issues are handled gracefully with retries

## Monitoring

### Queue Statistics
- Pending jobs count
- Running jobs count
- Completed jobs count
- Failed jobs count
- Oldest pending job information

### Job Details
- Job ID and type
- Status and priority
- Progress information
- Error messages
- Timestamps

### Processor Status
- Process ID
- Running status
- Thread health
- Shutdown status

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Job Parameters
Jobs can include custom parameters in the `job_parameters` JSON field:
```json
{
  "access_token": "google_token",
  "include_trashed": false,
  "custom_setting": "value"
}
```

## Troubleshooting

### Common Issues

1. **Jobs Not Processing**
   - Check if processor is running: `GET /job-queue/status`
   - Check for stuck jobs in "running" status
   - Restart processor if needed

2. **High Memory Usage**
   - Reduce concurrent processors
   - Check for memory leaks in job processing

3. **Database Lock Issues**
   - Check for long-running transactions
   - Ensure proper database connection pooling

### Logs

Job processor logs are written to:
- Console output
- `job_processor.log` file (when running standalone)

### Reset Stuck Jobs

Use the existing endpoint to reset stuck jobs:
```http
POST /indexing/reset-stuck-jobs/{program_id}
```

## Performance Considerations

- **Sequential Processing**: Jobs are processed one at a time to avoid resource conflicts
- **Database Indexes**: Proper indexes are created for efficient job selection
- **Connection Pooling**: Database connections are properly managed
- **Memory Management**: Large files are processed in chunks to avoid memory issues

## Security

- **Job Access Control**: Users can only access jobs for programs they have permission to
- **Process Isolation**: Each processor runs in its own thread
- **Token Security**: Google access tokens are stored securely and not logged

## Future Enhancements

- **Job Scheduling**: Support for scheduled jobs (cron-like)
- **Job Dependencies**: Support for job chains and dependencies
- **Load Balancing**: Better distribution of jobs across multiple processors
- **Metrics**: Detailed performance metrics and monitoring
- **Webhooks**: Notifications when jobs complete or fail

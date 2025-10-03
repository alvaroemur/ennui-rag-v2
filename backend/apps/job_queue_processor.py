"""
Job Queue Processor - Processes indexing jobs from database queue
"""
import gc
import json
import logging
import os
import psutil
import signal
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database.database import SessionLocal
from database.models import IndexingJob, Program, UserModel
from apps.google_drive import GoogleDriveScanner
from apps.indexing_service import IndexingService
from memory_monitor import get_memory_monitor, log_memory_usage

logger = logging.getLogger(__name__)


class JobQueueProcessor:
    """Processes jobs from the database queue sequentially"""
    
    def __init__(self, process_id: Optional[str] = None):
        self.process_id = process_id or f"processor_{uuid.uuid4().hex[:8]}"
        self.running = False
        self.thread = None
        self.shutdown_event = threading.Event()
        
        # Memory management settings
        self.max_file_size_mb = 100  # Maximum file size to process (MB)
        self.memory_cleanup_interval = 100  # Cleanup memory every N files
        self.files_processed_since_cleanup = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"JobQueueProcessor {self.process_id} initialized with memory management")
        
        # Setup memory monitoring
        self.memory_monitor = get_memory_monitor()
        self.memory_monitor.add_cleanup_callback(self._cleanup_memory)
        
        self._log_memory_usage("Processor initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.stop()
    
    def _log_memory_usage(self, context: str = ""):
        """Log current memory usage for monitoring"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            memory_percent = process.memory_percent()
            
            logger.info(f"🧠 Memory usage {context}: {memory_mb:.1f}MB ({memory_percent:.1f}%) - PID: {process.pid}")
            
            # Log memory warning if usage is high
            if memory_percent > 80:
                logger.warning(f"⚠️ High memory usage detected: {memory_percent:.1f}% - Consider cleanup")
            elif memory_percent > 60:
                logger.info(f"📊 Moderate memory usage: {memory_percent:.1f}%")
                
        except Exception as e:
            logger.error(f"Error logging memory usage: {str(e)}")
    
    def _cleanup_memory(self, force: bool = False):
        """Clean up memory and run garbage collection"""
        try:
            if force or self.files_processed_since_cleanup >= self.memory_cleanup_interval:
                logger.info(f"🧹 Running memory cleanup (processed {self.files_processed_since_cleanup} files)")
                
                # Force garbage collection
                collected = gc.collect()
                
                # Log memory before and after cleanup
                self._log_memory_usage("before cleanup")
                
                # Reset counter
                self.files_processed_since_cleanup = 0
                
                # Log cleanup results
                logger.info(f"🗑️ Garbage collection completed, collected {collected} objects")
                self._log_memory_usage("after cleanup")
                
        except Exception as e:
            logger.error(f"Error during memory cleanup: {str(e)}")
    
    def _should_skip_file(self, file_data: Dict) -> bool:
        """Check if file should be skipped (currently no files are skipped)"""
        # No files are skipped - all files are processed
        return False
    
    def start(self):
        """Start the job processor in a separate thread"""
        if self.running:
            logger.warning("Job processor is already running")
            return
        
        self.running = True
        self.shutdown_event.clear()
        
        # Start memory monitoring
        self.memory_monitor.start_monitoring(interval=30)
        
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        logger.info(f"Job processor {self.process_id} started with memory monitoring")
    
    def stop(self):
        """Stop the job processor gracefully"""
        if not self.running:
            return
        
        logger.info(f"Stopping job processor {self.process_id}...")
        self.running = False
        self.shutdown_event.set()
        
        # Stop memory monitoring
        self.memory_monitor.stop_monitoring()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=30)  # Wait up to 30 seconds
        
        # Final memory cleanup
        self._cleanup_memory(force=True)
        
        logger.info(f"Job processor {self.process_id} stopped")
    
    def _process_loop(self):
        """Main processing loop - runs in separate thread"""
        logger.info(f"🔄 Job processing loop started for {self.process_id}")
        self._log_memory_usage("Processing loop started")
        
        while self.running and not self.shutdown_event.is_set():
            try:
                # Log memory usage periodically
                self._log_memory_usage("Processing loop iteration")
                
                # Log queue status before checking for jobs
                queue_status = self._get_queue_status()
                logger.info(f"📊 Queue status - Pending: {queue_status['pending_jobs']}, Running: {queue_status['running_jobs']}, Completed: {queue_status['completed_jobs']}, Failed: {queue_status['failed_jobs']}")
                
                # Get next job from queue
                job = self._get_next_job()
                
                if job:
                    logger.info(f"🚀 Starting job {job.id} (type: {job.job_type}, priority: {job.priority}) for program {job.program_id}")
                    self._log_memory_usage(f"Before processing job {job.id}")
                    
                    self._process_job(job)
                    
                    logger.info(f"✅ Completed job {job.id} processing")
                    self._log_memory_usage(f"After processing job {job.id}")
                    
                    # Cleanup memory after each job
                    self._cleanup_memory(force=True)
                else:
                    # No jobs available, wait a bit
                    logger.debug(f"⏳ No jobs available, waiting... (Queue: {queue_status['pending_jobs']} pending)")
                    self.shutdown_event.wait(5)  # Wait 5 seconds or until shutdown
                    
            except Exception as e:
                logger.error(f"❌ Error in job processing loop: {str(e)}")
                self._log_memory_usage("After error in processing loop")
                self.shutdown_event.wait(30)  # Wait before retrying
        
        logger.info(f"🛑 Job processing loop ended for {self.process_id}")
        self._log_memory_usage("Processing loop ended")
    
    def _get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        db = SessionLocal()
        try:
            pending_count = db.query(IndexingJob).filter(IndexingJob.status == "pending").count()
            running_count = db.query(IndexingJob).filter(IndexingJob.status == "running").count()
            completed_count = db.query(IndexingJob).filter(IndexingJob.status == "completed").count()
            failed_count = db.query(IndexingJob).filter(IndexingJob.status == "failed").count()
            
            return {
                "pending_jobs": pending_count,
                "running_jobs": running_count,
                "completed_jobs": completed_count,
                "failed_jobs": failed_count
            }
        except Exception as e:
            logger.error(f"Error getting queue status: {str(e)}")
            return {"pending_jobs": 0, "running_jobs": 0, "completed_jobs": 0, "failed_jobs": 0}
        finally:
            db.close()

    def _get_next_job(self) -> Optional[IndexingJob]:
        """Get the next job from the queue (FIFO with priority)"""
        db = SessionLocal()
        try:
            # Get jobs that are pending and scheduled (or no schedule)
            now = datetime.utcnow()
            
            job = db.query(IndexingJob).filter(
                and_(
                    IndexingJob.status == "pending",
                    or_(
                        IndexingJob.scheduled_at.is_(None),
                        IndexingJob.scheduled_at <= now
                    )
                )
            ).order_by(
                IndexingJob.priority.desc(),  # Higher priority first
                IndexingJob.created_at.asc()  # FIFO within same priority
            ).first()
            
            if job:
                # Lock the job to prevent other processors from taking it
                job.status = "running"
                job.locked_at = now
                job.locked_by = self.process_id
                job.started_at = now
                db.commit()
                logger.info(f"🔒 Locked job {job.id} for processing by {self.process_id}")
            
            return job
            
        except Exception as e:
            logger.error(f"Error getting next job: {str(e)}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def _process_job(self, job: IndexingJob):
        """Process a single job"""
        db = SessionLocal()
        start_time = datetime.utcnow()
        
        try:
            logger.info(f"🔄 Starting processing of job {job.id} (type: {job.job_type}, priority: {job.priority})")
            
            # Get job parameters
            job_params = self._parse_job_parameters(job.job_parameters)
            access_token = job_params.get("access_token")
            include_trashed = job_params.get("include_trashed", False)
            
            logger.info(f"📋 Job {job.id} parameters - include_trashed: {include_trashed}, has_access_token: {bool(access_token)}")
            
            if not access_token:
                # Get access token from user
                user = db.query(UserModel).filter(UserModel.id == job.user_id).first()
                if not user or not user.google_access_token:
                    raise Exception("No Google access token available")
                access_token = user.google_access_token
                logger.info(f"🔑 Retrieved access token from user {user.id} for job {job.id}")
            
            # Get program
            program = db.query(Program).filter(Program.id == job.program_id).first()
            if not program:
                raise Exception("Program not found")
            
            logger.info(f"📁 Processing job {job.id} for program '{program.name}' (ID: {program.id})")
            
            # Create indexing service and process the job
            indexing_service = IndexingService(db)
            
            # Process the job synchronously (no async)
            self._process_indexing_job_sync(
                indexing_service, 
                job, 
                program, 
                access_token, 
                include_trashed
            )
            
            # Mark job as completed
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.locked_at = None
            job.locked_by = None
            db.commit()
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Job {job.id} completed successfully in {processing_time:.2f} seconds - Processed: {job.processed_files}, Successful: {job.successful_files}, Failed: {job.failed_files}")
            
        except Exception as e:
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"❌ Error processing job {job.id} after {processing_time:.2f} seconds: {str(e)}")
            
            try:
                # Handle retry logic
                job.retry_count += 1
                job.error_message = str(e)[:1000]  # Limit error message length
                
                if job.retry_count < job.max_retries:
                    # Retry the job
                    job.status = "pending"
                    job.scheduled_at = datetime.utcnow() + timedelta(minutes=5)  # Retry in 5 minutes
                    job.locked_at = None
                    job.locked_by = None
                    logger.warning(f"🔄 Job {job.id} will be retried in 5 minutes ({job.retry_count}/{job.max_retries}) - Error: {str(e)[:200]}")
                else:
                    # Max retries exceeded, mark as failed
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.locked_at = None
                    job.locked_by = None
                    logger.error(f"💥 Job {job.id} failed permanently after {job.max_retries} retries - Final error: {str(e)[:200]}")
                
                db.commit()
            except Exception as commit_error:
                logger.error(f"❌ Error committing job status update for job {job.id}: {str(commit_error)}")
                db.rollback()
        
        finally:
            db.close()
    
    def _process_indexing_job_sync(
        self, 
        indexing_service: IndexingService,
        job: IndexingJob, 
        program: Program, 
        access_token: str, 
        include_trashed: bool
    ):
        """Process indexing job synchronously (converted from async)"""
        try:
            # Update job status
            job.status = "running"
            job.started_at = datetime.utcnow()
            
            # Create Google Drive scanner
            scanner = GoogleDriveScanner(access_token)
            folder_id = job.folder_id or program.drive_folder_id
            
            logger.info(f"🔍 Starting Google Drive scan for program {program.id}, folder {folder_id} (include_trashed: {include_trashed})")
            
            # Scan folder (this needs to be converted to sync)
            files = self._scan_folder_sync(scanner, folder_id, include_trashed)
            
            # Update counters
            job.total_files = len(files)
            job.processed_files = 0
            job.successful_files = 0
            job.failed_files = 0
            
            logger.info(f"📊 Found {job.total_files} files to process for job {job.id}")
            
            # Process each file with memory management
            for i, file_data in enumerate(files, 1):
                file_id = file_data.get('id', 'unknown')
                file_name = file_data.get('name', 'unnamed')
                file_size_mb = file_data.get('size', 0) / (1024 * 1024)
                
                logger.info(f"📄 Processing file {i} of {len(files)} for job {job.id}: {file_name} ({file_size_mb:.1f}MB)")
                
                try:
                    # Process all files (including large files and videos) with memory optimization
                    self._process_file_sync(indexing_service, job, program, file_data, scanner)
                    job.successful_files += 1
                    
                    # Increment processed files counter
                    self.files_processed_since_cleanup += 1
                    
                    # Log progress every 10 files or for important milestones
                    if job.processed_files % 10 == 0 or i == len(files):
                        progress_pct = (job.processed_files / job.total_files) * 100 if job.total_files > 0 else 0
                        logger.info(f"📈 Job {job.id} progress: {job.processed_files}/{job.total_files} files ({progress_pct:.1f}%) - ✅ {job.successful_files} successful, ❌ {job.failed_files} failed")
                        
                        # Log memory usage during progress
                        self._log_memory_usage(f"Job {job.id} progress checkpoint")
                        
                except Exception as e:
                    logger.error(f"❌ Error processing file {file_id} ({file_name}): {str(e)}")
                    job.failed_files += 1
                    
                    # Create failed file record
                    self._create_failed_file_record_sync(indexing_service, job, file_data, str(e))
                
                job.processed_files += 1
                
                # Update progress and commit every 10 files
                if job.processed_files % 10 == 0:
                    indexing_service.db.commit()
                    
                    # Run memory cleanup periodically
                    self._cleanup_memory()
            
            # Final memory cleanup after processing all files
            self._cleanup_memory(force=True)
            
            logger.info(f"🎉 Indexing job {job.id} completed! Processed: {job.processed_files}, Successful: {job.successful_files}, Failed: {job.failed_files}")
            
        except Exception as e:
            logger.error(f"💥 Error in indexing job {job.id}: {str(e)}")
            raise
    
    def _scan_folder_sync(self, scanner: GoogleDriveScanner, folder_id: str, include_trashed: bool):
        """Synchronous version of folder scanning with proper memory management"""
        import asyncio
        
        async def _async_scan():
            try:
                logger.info(f"🔍 Starting folder scan for folder {folder_id} (include_trashed: {include_trashed})")
                self._log_memory_usage("Before folder scan")
                
                files = await scanner.scan_folder_recursive(folder_id, include_trashed)
                
                logger.info(f"📁 Folder scan completed, found {len(files)} files")
                self._log_memory_usage("After folder scan")
                
                return files
            except Exception as e:
                logger.error(f"❌ Error during folder scan: {str(e)}")
                self._log_memory_usage("After folder scan error")
                raise
        
        # Use asyncio.run() instead of creating new event loops to prevent memory leaks
        try:
            return asyncio.run(_async_scan())
        except Exception as e:
            logger.error(f"❌ Failed to scan folder {folder_id}: {str(e)}")
            return []
    
    def _process_file_sync(
        self, 
        indexing_service: IndexingService,
        job: IndexingJob, 
        program: Program, 
        file_data: Dict, 
        scanner: GoogleDriveScanner
    ):
        """Synchronous version of file processing with memory management"""
        import asyncio
        
        # Check if file should be skipped (currently no files are skipped)
        if self._should_skip_file(file_data):
            return
        
        async def _async_process():
            try:
                file_id = file_data.get('id', 'unknown')
                file_name = file_data.get('name', 'unnamed')
                
                logger.debug(f"📄 Processing file: {file_name} (ID: {file_id})")
                self._log_memory_usage(f"Before processing file {file_id}")
                
                await indexing_service._process_file(job, program, file_data, scanner)
                
                logger.debug(f"✅ File processed successfully: {file_name}")
                self._log_memory_usage(f"After processing file {file_id}")
                
            except Exception as e:
                logger.error(f"❌ Error processing file {file_data.get('id', 'unknown')}: {str(e)}")
                self._log_memory_usage(f"After file processing error for {file_data.get('id', 'unknown')}")
                raise
        
        # Use asyncio.run() instead of creating new event loops to prevent memory leaks
        try:
            asyncio.run(_async_process())
        except Exception as e:
            logger.error(f"❌ Failed to process file {file_data.get('id', 'unknown')}: {str(e)}")
            raise
    
    def _create_failed_file_record_sync(
        self, 
        indexing_service: IndexingService,
        job: IndexingJob, 
        file_data: Dict, 
        error_message: str
    ):
        """Synchronous version of creating failed file record"""
        indexing_service._create_failed_file_record(job, file_data, error_message)
    
    def _parse_job_parameters(self, job_parameters: Optional[str]) -> Dict[str, Any]:
        """Parse job parameters from JSON string"""
        if not job_parameters:
            return {}
        
        try:
            return json.loads(job_parameters)
        except (json.JSONDecodeError, TypeError):
            logger.warning(f"Invalid job parameters JSON: {job_parameters}")
            return {}
    
    def is_running(self) -> bool:
        """Check if the processor is running"""
        return self.running and self.thread and self.thread.is_alive()
    
    def get_status(self) -> Dict[str, Any]:
        """Get processor status"""
        return {
            "process_id": self.process_id,
            "running": self.running,
            "thread_alive": self.thread.is_alive() if self.thread else False,
            "shutdown_requested": self.shutdown_event.is_set()
        }


# Global processor instance
_processor: Optional[JobQueueProcessor] = None


def get_processor() -> JobQueueProcessor:
    """Get the global job processor instance"""
    global _processor
    if _processor is None:
        _processor = JobQueueProcessor()
    return _processor


def start_processor():
    """Start the global job processor"""
    processor = get_processor()
    processor.start()


def stop_processor():
    """Stop the global job processor"""
    global _processor
    if _processor:
        _processor.stop()
        _processor = None


def is_processor_running() -> bool:
    """Check if the processor is running"""
    return _processor is not None and _processor.is_running()


def get_processor_status() -> Dict[str, Any]:
    """Get processor status"""
    if _processor:
        return _processor.get_status()
    return {"process_id": None, "running": False, "thread_alive": False, "shutdown_requested": False}


# CLI interface for running the processor as a standalone service
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Job Queue Processor")
    parser.add_argument("--process-id", help="Process ID for this processor instance")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start processor
    processor = JobQueueProcessor(process_id=args.process_id)
    
    try:
        processor.start()
        
        if args.daemon:
            # Keep running until interrupted
            while processor.is_running():
                time.sleep(1)
        else:
            # Run for a specific time or until interrupted
            time.sleep(3600)  # Run for 1 hour
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        processor.stop()
        logger.info("Processor stopped")

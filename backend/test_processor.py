#!/usr/bin/env python3
"""
Test script to debug the job processor
"""
import logging
import time
from apps.job_queue_processor import start_processor, is_processor_running, get_processor_status
from database.database import SessionLocal
from database.models import IndexingJob

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_processor():
    """Test the job processor"""
    try:
        logger.info("Testing job processor...")
        
        # Check current queue status
        db = SessionLocal()
        try:
            pending_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'pending').count()
            running_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'running').count()
            logger.info(f"Queue status - Pending: {pending_jobs}, Running: {running_jobs}")
        finally:
            db.close()
        
        # Start processor
        logger.info("Starting processor...")
        start_processor()
        
        # Check if running
        logger.info(f"Processor running: {is_processor_running()}")
        logger.info(f"Processor status: {get_processor_status()}")
        
        # Wait and check again
        logger.info("Waiting 5 seconds...")
        time.sleep(5)
        
        logger.info(f"Processor still running: {is_processor_running()}")
        
        # Check queue status again
        db = SessionLocal()
        try:
            pending_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'pending').count()
            running_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'running').count()
            completed_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'completed').count()
            failed_jobs = db.query(IndexingJob).filter(IndexingJob.status == 'failed').count()
            logger.info(f"Final queue status - Pending: {pending_jobs}, Running: {running_jobs}, Completed: {completed_jobs}, Failed: {failed_jobs}")
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_processor()

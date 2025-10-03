#!/usr/bin/env python3
"""
Standalone Job Queue Processor
Run this script to process indexing jobs from the database queue
"""
import argparse
import logging
import signal
import sys
import time
from apps.job_queue_processor import JobQueueProcessor

def setup_logging(level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('job_processor.log')
        ]
    )

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Job Queue Processor")
    parser.add_argument("--process-id", help="Process ID for this processor instance")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help="Log level")
    parser.add_argument("--daemon", action="store_true", 
                       help="Run as daemon (keep running until interrupted)")
    parser.add_argument("--timeout", type=int, default=0,
                       help="Run for specified seconds (0 = run indefinitely)")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(getattr(logging, args.log_level))
    logger = logging.getLogger(__name__)
    
    # Create processor
    processor = JobQueueProcessor(process_id=args.process_id)
    
    try:
        logger.info(f"Starting job processor with ID: {processor.process_id}")
        processor.start()
        
        if args.daemon or args.timeout == 0:
            # Run indefinitely until interrupted
            logger.info("Running in daemon mode - press Ctrl+C to stop")
            while processor.is_running():
                time.sleep(1)
        else:
            # Run for specified timeout
            logger.info(f"Running for {args.timeout} seconds")
            time.sleep(args.timeout)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Stopping job processor...")
        processor.stop()
        logger.info("Job processor stopped")

if __name__ == "__main__":
    main()

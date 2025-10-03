#!/usr/bin/env python3
"""
Startup script that ensures the job processor starts with the API
"""
import uvicorn
import logging
from apps.job_queue_processor import start_processor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_app():
    """Start the app with job processor"""
    try:
        logger.info("🚀 Starting app with job processor...")
        
        # Start the job processor
        start_processor()
        logger.info("✅ Job processor started successfully")
        
        # Start the API
        logger.info("🌐 Starting FastAPI server...")
        uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
        
    except Exception as e:
        logger.error(f"❌ Error starting app: {str(e)}")
        raise

if __name__ == "__main__":
    start_app()

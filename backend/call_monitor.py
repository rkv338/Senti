#!/usr/bin/env python3
"""
Call Monitor Service
Run this script to continuously monitor Redis for scheduled calls
"""

import logging
import signal
import sys
from scheduler import start_call_monitor, stop_call_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('call_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal. Stopping call monitor...")
    stop_call_monitor()
    sys.exit(0)

def main():
    """Main function to start the call monitoring service"""
    logger.info("Starting Call Monitor Service...")
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    try:
        # Start the call monitor
        start_call_monitor()
        
        logger.info("Call monitor is running. Press Ctrl+C to stop.")
        
        # Keep the script running
        while True:
            signal.pause()
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
        stop_call_monitor()
    except Exception as e:
        logger.error(f"Error in call monitor: {e}")
        stop_call_monitor()
        sys.exit(1)

if __name__ == "__main__":
    main()

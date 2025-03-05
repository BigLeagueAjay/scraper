"""
Error Handler module for the Web Scraper

This module handles errors and logging for the application.
"""

import logging
import os
import sys
import traceback
from typing import Optional
from datetime import datetime

def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """
    Set up logging for the application.
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file (optional)
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    else:
        # Default log file in logs directory
        logs_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = os.path.join(logs_dir, f"scraper_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set third-party loggers to a higher level to reduce noise
    for logger_name in ['urllib3', 'asyncio', 'playwright']:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    
    logging.info(f"Logging initialized at level {log_level}")
    logging.info(f"Log file: {log_file}")

def handle_exception(exception: Exception, exit_app: bool = False):
    """
    Handle exceptions in a consistent way.
    
    Args:
        exception: The exception to handle
        exit_app: Whether to exit the application after handling
    """
    logger = logging.getLogger(__name__)
    
    # Get the exception details
    exc_type = type(exception).__name__
    exc_message = str(exception)
    exc_traceback = traceback.format_exc()
    
    # Log the exception
    logger.error(f"{exc_type}: {exc_message}")
    logger.debug(f"Traceback: {exc_traceback}")
    
    # Print user-friendly message
    print(f"Error: {exc_message}", file=sys.stderr)
    
    # Handle specific exception types
    if isinstance(exception, ImportError):
        print("This error may be due to missing dependencies. "
              "Please ensure you have installed all required packages.", file=sys.stderr)
    elif isinstance(exception, ConnectionError):
        print("This error may be due to connection issues. "
              "Please check your internet connection and try again.", file=sys.stderr)
    elif isinstance(exception, TimeoutError):
        print("The operation timed out. "
              "This may be due to a slow server or internet connection.", file=sys.stderr)
    
    # Exit if requested
    if exit_app:
        logger.info("Exiting application due to error")
        sys.exit(1)

class ScraperError(Exception):
    """Base class for scraper-specific exceptions."""
    pass

class ConfigurationError(ScraperError):
    """Exception raised for errors in the configuration."""
    pass

class CrawlError(ScraperError):
    """Exception raised for errors during crawling."""
    pass

class ProcessingError(ScraperError):
    """Exception raised for errors during content processing."""
    pass

class FileError(ScraperError):
    """Exception raised for errors during file operations."""
    pass

class AuthenticationError(ScraperError):
    """Exception raised for authentication errors."""
    pass
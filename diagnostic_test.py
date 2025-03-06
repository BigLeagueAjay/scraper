#!/usr/bin/env python3
"""
Diagnostic test script for the web scraper application.
This script will help identify potential issues in the codebase.
"""

import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("diagnostic")

def test_imports():
    """Test import consistency"""
    logger.info("Testing imports...")
    
    try:
        # Test direct import (as in crawler.py)
        logger.debug("Attempting direct import: from confluence_scraper import RobustCrawler")
        try:
            from confluence_scraper import RobustCrawler
            logger.info("✅ Direct import successful")
        except ImportError as e:
            logger.error(f"❌ Direct import failed: {e}")
            
        # Test src-prefixed import (as in cli.py)
        logger.debug("Attempting src-prefixed import: from src.confluence_scraper import RobustCrawler")
        try:
            from src.confluence_scraper import RobustCrawler
            logger.info("✅ src-prefixed import successful")
        except ImportError as e:
            logger.error(f"❌ src-prefixed import failed: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error during import tests: {e}")

def test_confluence_detection():
    """Test Confluence URL detection logic"""
    logger.info("Testing Confluence URL detection...")
    
    try:
        # Import both modules that do detection
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import the crawler module
        try:
            from src.crawler import Crawler
            
            # Create a minimal args object
            class Args:
                def __init__(self):
                    self.timeout = 30
                    self.render_js = True
                    self.wait_time = 5
            
            # Test URLs
            test_urls = [
                "https://confluence.example.com/display/SPACE/Page",
                "https://example.atlassian.net/wiki/spaces/SPACE/pages/123456",
                "https://example.com/some/page",
                "https://atlassian.net/some/other/page",
                "https://bigleagueinc.atlassian.net/l/cp/ru5nUbGr"
            ]
            
            # Create crawler instance
            crawler = Crawler(Args())
            
            # Test each URL
            for url in test_urls:
                is_confluence = crawler.is_confluence_url(url)
                logger.info(f"URL: {url} -> Detected as Confluence: {is_confluence}")
                
                # Also test CLI detection logic
                cli_detection = 'confluence' in url.lower() or 'atlassian.net' in url.lower()
                logger.info(f"URL: {url} -> CLI detection: {cli_detection}")
                
                # Check for inconsistency
                if is_confluence != cli_detection:
                    logger.warning(f"❌ Inconsistent detection for {url}: crawler={is_confluence}, cli={cli_detection}")
                else:
                    logger.info(f"✅ Consistent detection for {url}")
                    
        except ImportError as e:
            logger.error(f"Could not import Crawler: {e}")
            
    except Exception as e:
        logger.error(f"Unexpected error during Confluence detection tests: {e}")

def test_page_id_extraction():
    """Test Confluence page ID extraction"""
    logger.info("Testing Confluence page ID extraction...")
    
    try:
        # Import the RobustCrawler
        try:
            from src.confluence_scraper import RobustCrawler
            
            # Create a minimal args object
            class Args:
                def __init__(self):
                    self.url = "https://example.com"
                    self.space = None
                    self.page_id = None
                    self.timeout = 60
                    self.render_js = True
                    self.wait_time = 10
            
            # Create crawler instance
            crawler = RobustCrawler(Args())
            
            # Test URLs with different page ID formats
            test_urls = [
                "https://confluence.example.com/display/SPACE/Page?pageId=123456",
                "https://example.atlassian.net/wiki/spaces/SPACE/pages/123456",
                "https://example.atlassian.net/l/cp/abcDEF123",
                "https://bigleagueinc.atlassian.net/l/cp/ru5nUbGr"
            ]
            
            # Test each URL
            for url in test_urls:
                page_id = crawler._extract_page_id(url)
                logger.info(f"URL: {url} -> Extracted page ID: {page_id}")
                
                if not page_id:
                    logger.warning(f"❌ Failed to extract page ID from {url}")
                else:
                    logger.info(f"✅ Successfully extracted page ID: {page_id}")
                    
        except ImportError as e:
            logger.error(f"Could not import RobustCrawler: {e}")
            
    except Exception as e:
        logger.error(f"Unexpected error during page ID extraction tests: {e}")

def test_entry_point():
    """Test the entry point configuration"""
    logger.info("Testing entry point configuration...")
    
    try:
        # Check the setup.py file
        with open("setup.py", "r") as f:
            setup_content = f.read()
            
        # Look for the entry point definition
        if "scrapemd=cli:main_cli" in setup_content:
            logger.warning("❌ Entry point may be incorrect: 'scrapemd=cli:main_cli'")
            logger.warning("   Should likely be: 'scrapemd=src.cli:main_cli'")
        elif "scrapemd=src.cli:main_cli" in setup_content:
            logger.info("✅ Entry point appears correct: 'scrapemd=src.cli:main_cli'")
        else:
            logger.warning("❓ Could not find expected entry point pattern")
            
    except Exception as e:
        logger.error(f"Unexpected error during entry point test: {e}")

if __name__ == "__main__":
    logger.info("Starting diagnostic tests...")
    
    # Run tests
    test_imports()
    print("\n" + "-"*50 + "\n")
    
    test_confluence_detection()
    print("\n" + "-"*50 + "\n")
    
    test_page_id_extraction()
    print("\n" + "-"*50 + "\n")
    
    test_entry_point()
    
    logger.info("Diagnostic tests completed.")
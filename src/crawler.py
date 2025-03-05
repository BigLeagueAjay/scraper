"""
Crawler module for the Web Scraper

This module wraps the crawl4ai library to handle the crawling of web pages.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import urllib.parse

# Import crawl4ai components
try:
    from crawl4ai import AsyncWebCrawler
except ImportError:
    raise ImportError(
        "crawl4ai package is not installed. Please install it with: pip install -U crawl4ai"
    )

logger = logging.getLogger(__name__)

class Crawler:
    """
    Wrapper around crawl4ai's AsyncWebCrawler for web crawling.
    """
    
    def __init__(self, args):
        """
        Initialize the crawler with the provided arguments.
        
        Args:
            args: Command line arguments
        """
        self.args = args
        self.timeout = getattr(args, 'timeout', 30)
        self.depth = getattr(args, 'depth', 1)
        self.username = getattr(args, 'username', None)
        self.password = getattr(args, 'password', None)
        self.is_confluence = getattr(args, 'confluence', False)
        self.space_key = getattr(args, 'space', None)
        self.page_id = getattr(args, 'page_id', None)
        
        # Configure the crawler
        self._setup_crawler()
        
    def _setup_crawler(self):
        """
        Set up the crawler with the appropriate configuration.
        """
        # Common crawl4ai options
        self.crawler_options = {
            "timeout": self.timeout,
        }
        
        # Configure authentication if provided
        if self.username and self.password:
            self.crawler_options["auth"] = {
                "username": self.username,
                "password": self.password
            }
        
        # Configure for Confluence if specified
        if self.is_confluence:
            logger.info("Configuring for Confluence crawling")
            self.crawler_options["confluence"] = True
            
            if self.space_key:
                self.crawler_options["space_key"] = self.space_key
                
            if self.page_id:
                self.crawler_options["page_id"] = self.page_id
        
        logger.debug(f"Crawler configured with options: {self.crawler_options}")
        
    async def crawl(self, url: str) -> Dict[str, Any]:
        """
        Crawl the specified URL and return the content.
        
        Args:
            url: The URL to crawl
            
        Returns:
            Dict containing the crawled content
        """
        logger.info(f"Starting crawl of {url}")
        
        try:
            # Create AsyncWebCrawler instance with our options
            async with AsyncWebCrawler() as crawler:
                # Configure the crawler options
                for key, value in self.crawler_options.items():
                    setattr(crawler, key, value)
                
                # Execute the crawl
                if self.depth > 1:
                    logger.info(f"Performing deep crawl with depth {self.depth}")
                    result = await crawler.arun(
                        url=url,
                        deep_crawl=True,
                        max_pages=self.depth
                    )
                else:
                    logger.info("Performing single page crawl")
                    result = await crawler.arun(url=url)
                
                logger.info(f"Crawl completed successfully for {url}")
                return result
                
        except Exception as e:
            logger.error(f"Error during crawl: {str(e)}")
            raise RuntimeError(f"Failed to crawl {url}: {str(e)}")
    
    def extract_domain(self, url: str) -> str:
        """
        Extract the domain from a URL.
        
        Args:
            url: The URL to extract domain from
            
        Returns:
            str: The domain name
        """
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc
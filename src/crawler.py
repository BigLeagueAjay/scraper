"""
Crawler module for the Web Scraper

This module wraps the crawl4ai library to handle the crawling of web pages with
improved content extraction capabilities.
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

# Import additional dependencies for enhanced extraction
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
    logging.warning("BeautifulSoup is not installed. Enhanced content extraction will be limited.")

logger = logging.getLogger(__name__)

class Crawler:
    """
    Wrapper around crawl4ai's AsyncWebCrawler for web crawling with enhanced
    content extraction capabilities.
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
        self.render_js = getattr(args, 'render_js', True)
        self.wait_time = getattr(args, 'wait_time', 5)
        
        # Configure the crawler
        self._setup_crawler()
        
    def _setup_crawler(self):
        """
        Set up the crawler with enhanced configuration for better content extraction.
        """
        # Enhanced crawl4ai options
        self.crawler_options = {
            "timeout": self.timeout,
            "javascript": self.render_js,  # Enable JavaScript rendering
            "wait_for": self.wait_time,    # Wait for dynamic content to load
            "retry_count": 3,              # Retry failed requests
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
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
        Crawl the specified URL and return the content with enhanced extraction.
        
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
                
                # Special handling for documentation sites
                if "docs." in url or "/documentation" in url:
                    logger.info("Documentation site detected, adjusting crawler settings")
                    # Increase wait time for documentation sites which often have complex rendering
                    setattr(crawler, "wait_for", max(self.wait_time, 8))
                    setattr(crawler, "javascript", True)
                
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
                
                # Convert CrawlResult object to a dictionary
                result_dict = self._process_crawl_result(result, url)
                
                # Apply enhanced content extraction if needed
                if not result_dict.get('content') or result_dict.get('content') == "Error: No content could be extracted.":
                    result_dict = self._enhance_content_extraction(result, result_dict)
                
                return result_dict
                
        except Exception as e:
            logger.error(f"Error during crawl: {str(e)}")
            raise RuntimeError(f"Failed to crawl {url}: {str(e)}")
    
    def _process_crawl_result(self, result, url) -> Dict[str, Any]:
        """
        Process the CrawlResult object and convert it to a dictionary.
        
        Args:
            result: The CrawlResult object
            url: The original URL
            
        Returns:
            Dict containing processed crawl data
        """
        # First check if it has a to_dict method
        if hasattr(result, 'to_dict') and callable(getattr(result, 'to_dict')):
            return result.to_dict()
        
        # If not, create a dictionary from common attributes
        result_dict = {}
        
        # Extract common attributes
        for attr in ['content', 'title', 'html', 'text', 'links', 'status', 'headers']:
            if hasattr(result, attr):
                result_dict[attr] = getattr(result, attr)
        
        # Add the original URL
        result_dict['url'] = url
        
        # Special handling for nested data if available
        if hasattr(result, 'data') and result.data is not None:
            result_dict['data'] = result.data
        
        # If result has metadata
        if hasattr(result, 'metadata') and result.metadata is not None:
            result_dict['metadata'] = result.metadata
        
        # Store all available attribute names for debugging
        result_dict['available_attributes'] = dir(result)
        
        logger.debug(f"Converted CrawlResult to dictionary with keys: {result_dict.keys()}")
        return result_dict
    
    def _enhance_content_extraction(self, result, result_dict) -> Dict[str, Any]:
        """
        Apply enhanced content extraction techniques when standard extraction fails.
        
        Args:
            result: The original CrawlResult object
            result_dict: The current result dictionary
            
        Returns:
            Dict with enhanced content extraction
        """
        # Try to extract content from HTML if available
        if hasattr(result, 'html') and result.html and BeautifulSoup is not None:
            html = result.html
            logger.info("Applying enhanced content extraction with BeautifulSoup")
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements that might interfere with text extraction
            for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
                script_or_style.decompose()
            
            # Try multiple strategies to find main content
            content = None
            
            # Strategy 1: Look for main content containers
            for selector in ['main', 'article', '.content', '#content', '.main-content', '.documentation', '.docs-content']:
                main_content = soup.select(selector)
                if main_content:
                    content = main_content[0].get_text(strip=True)
                    logger.info(f"Content extracted using selector: {selector}")
                    break
            
            # Strategy 2: If no content found, try to extract all paragraphs
            if not content:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
                    logger.info("Content extracted from paragraphs")
            
            # Strategy 3: Last resort, get all text
            if not content:
                content = soup.get_text(separator='\n', strip=True)
                logger.info("Content extracted from full page text")
            
            # Update the dictionary with extracted content
            if content and len(content) > 50:  # Ensure we have meaningful content
                result_dict['content'] = content
                result_dict['extraction_method'] = 'enhanced'
                logger.info(f"Enhanced extraction successful, extracted {len(content)} characters")
            else:
                logger.warning("Enhanced extraction failed to find meaningful content")
        else:
            logger.warning("Enhanced extraction failed: HTML not available or BeautifulSoup not installed")
        
        return result_dict
    
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
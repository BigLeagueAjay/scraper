#!/usr/bin/env python3
"""
Web Scraper with crawl4ai

A command-line application that takes a URL as input, scrapes the content 
of the webpage, and converts it into a markdown file.
"""

import argparse
import asyncio
import logging
import sys
from urllib.parse import urlparse

# Import local modules
from src.cli import parse_arguments
from src.crawler import Crawler
from src.processor import ContentProcessor
from src.file_manager import FileManager
from src.error_handler import setup_logging, handle_exception

async def main():
    """Main entry point for the web scraper application."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        logger.info(f"Starting scrape of {args.url}")
        
        # Initialize components
        crawler = Crawler(args)
        processor = ContentProcessor()
        file_manager = FileManager(args.output if hasattr(args, 'output') else None)
        
        # Crawl the URL
        result = await crawler.crawl(args.url)
        
        # Process the content
        markdown_content = processor.process(result)
        
        # Generate filename from URL/title
        domain = urlparse(args.url).netloc
        title = result.get('title', 'unnamed_page')
        
        # Save the content
        output_path = file_manager.save(markdown_content, domain, title)
        
        logger.info(f"Successfully saved markdown to {output_path}")
        print(f"Content scraped and saved to: {output_path}")
        
    except Exception as e:
        handle_exception(e)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
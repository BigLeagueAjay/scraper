"""
Command Line Interface module for the Web Scraper

This module handles the parsing of command line arguments.
"""

import argparse
import os
from urllib.parse import urlparse


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Web Scraper with crawl4ai - Convert web pages to markdown",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        "--url", 
        required=True,
        help="URL of the webpage to scrape"
    )
    
    # Optional arguments
    parser.add_argument(
        "--output", 
        default="./scraped_content",
        help="Directory to save the output files"
    )
    
    parser.add_argument(
        "--depth", 
        type=int, 
        default=1,
        help="Depth of crawling (1 for single page, >1 for recursive)"
    )
    
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=30,
        help="Timeout in seconds for HTTP requests"
    )
    
    # Authentication options
    auth_group = parser.add_argument_group('Authentication Options')
    
    auth_group.add_argument(
        "--username", 
        help="Username for authentication"
    )
    
    auth_group.add_argument(
        "--password", 
        help="Password for authentication"
    )
    
    # Confluence specific options
    confluence_group = parser.add_argument_group('Confluence Options')
    
    confluence_group.add_argument(
        "--confluence", 
        action="store_true",
        help="Specify if the target is a Confluence site"
    )
    
    confluence_group.add_argument(
        "--space", 
        help="Confluence space key"
    )
    
    confluence_group.add_argument(
        "--page-id", 
        help="Confluence page ID"
    )
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    
    advanced_group.add_argument(
        "--config", 
        help="Path to configuration file"
    )
    
    advanced_group.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    advanced_group.add_argument(
        "--force", 
        action="store_true",
        help="Force overwrite existing files"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate URL
    try:
        parsed_url = urlparse(args.url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            parser.error("Invalid URL format. Please provide a complete URL including scheme (e.g., https://)")
    except Exception:
        parser.error("Invalid URL provided")
    
    # Validate output directory
    args.output = os.path.abspath(args.output)
    
    # Validate Confluence options
    if args.confluence and not (args.space or args.page_id):
        parser.error("Confluence mode requires either --space or --page-id")
    
    # Validate authentication
    if (args.username and not args.password) or (args.password and not args.username):
        parser.error("Both username and password must be provided for authentication")
    
    return args
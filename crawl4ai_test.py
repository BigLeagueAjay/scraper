#!/usr/bin/env python3
"""
Test script to explore the CrawlResult object from crawl4ai.
"""

import asyncio
from crawl4ai import AsyncWebCrawler
import inspect

async def test_crawl4ai():
    """Test crawl4ai and explore the CrawlResult object."""
    print("Testing crawl4ai...")
    
    async with AsyncWebCrawler() as crawler:
        # Set some options
        crawler.timeout = 30
        crawler.javascript = True
        crawler.wait_for = 5
        
        # Crawl a simple URL
        result = await crawler.arun(url="https://example.com")
        
        # Print the type of the result
        print(f"Result type: {type(result)}")
        
        # Print all attributes of the result
        print("\nAttributes:")
        for attr in dir(result):
            if not attr.startswith('_'):  # Skip private attributes
                try:
                    value = getattr(result, attr)
                    # If it's a method, skip it
                    if not inspect.ismethod(value):
                        print(f"  {attr}: {type(value)}")
                        # If it's a string, print a preview
                        if isinstance(value, str) and value:
                            preview = value[:100] + "..." if len(value) > 100 else value
                            print(f"    Preview: {preview}")
                except Exception as e:
                    print(f"  {attr}: Error accessing - {e}")
        
        # Try to access specific attributes mentioned in the error
        print("\nSpecific attributes:")
        try:
            print(f"  result.content exists: {'content' in dir(result)}")
            if 'content' in dir(result):
                print(f"  result.content: {result.content[:100]}...")
        except Exception as e:
            print(f"  Error accessing result.content: {e}")
            
        try:
            print(f"  result.text exists: {'text' in dir(result)}")
            if 'text' in dir(result):
                print(f"  result.text: {result.text[:100]}...")
        except Exception as e:
            print(f"  Error accessing result.text: {e}")
            
        # Check for other possible content attributes
        possible_attrs = ['html', 'body', 'raw_html', 'raw_text', 'markdown']
        print("\nOther possible content attributes:")
        for attr in possible_attrs:
            try:
                if hasattr(result, attr):
                    value = getattr(result, attr)
                    if value:
                        preview = value[:100] + "..." if len(value) > 100 else value
                        print(f"  result.{attr}: {preview}")
                    else:
                        print(f"  result.{attr} exists but is empty")
                else:
                    print(f"  result.{attr} does not exist")
            except Exception as e:
                print(f"  Error accessing result.{attr}: {e}")

if __name__ == "__main__":
    asyncio.run(test_crawl4ai())
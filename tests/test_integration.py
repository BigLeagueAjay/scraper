"""
Integration tests for the Web Scraper application.
"""

import os
import unittest
import asyncio
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.cli import parse_arguments
from src.crawler import Crawler
from src.processor import ContentProcessor
from src.file_manager import FileManager

class TestIntegration(unittest.TestCase):
    """Integration test cases for the Web Scraper application."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test output
        self.test_dir = tempfile.mkdtemp()
        
        # Mock command line arguments
        self.test_url = "https://example.com"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.crawler.AsyncWebCrawler')
    async def test_end_to_end_workflow(self, mock_crawler_class, mock_parse_args):
        """Test the end-to-end workflow of the application."""
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.url = self.test_url
        mock_args.output = self.test_dir
        mock_args.depth = 1
        mock_args.timeout = 30
        mock_args.username = None
        mock_args.password = None
        mock_args.confluence = False
        mock_args.space = None
        mock_args.page_id = None
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args
        
        # Mock the crawler response
        mock_instance = MagicMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_instance
        mock_instance.arun.return_value = {
            'title': 'Example Domain',
            'url': self.test_url,
            'markdown': '# Example Domain\n\nThis domain is for use in illustrative examples in documents.',
            'timestamp': '2025-03-05 04:00:00'
        }
        
        # Initialize components
        crawler = Crawler(mock_args)
        processor = ContentProcessor()
        file_manager = FileManager(mock_args.output)
        
        # Execute the workflow
        result = await crawler.crawl(mock_args.url)
        markdown_content = processor.process(result)
        output_path = file_manager.save(markdown_content, 'example.com', 'Example Domain')
        
        # Verify the output file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Read the output file and verify its contents
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that the content contains expected elements
        self.assertIn('# Example Domain', content)
        self.assertIn('_Source: https://example.com_', content)
        self.assertIn('This domain is for use in illustrative examples in documents', content)

# Helper function to run async tests
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
            asyncio.set_event_loop(None)
    return wrapper

# Replace the test methods with the async_test decorator
TestIntegration.test_end_to_end_workflow = async_test(TestIntegration.test_end_to_end_workflow)

if __name__ == '__main__':
    unittest.main()
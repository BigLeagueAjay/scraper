"""
Tests for the Crawler module.
"""

import unittest
import asyncio
from unittest.mock import patch, MagicMock
from src.crawler import Crawler

class TestCrawler(unittest.TestCase):
    """Test cases for the Crawler class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a mock args object
        self.args = MagicMock()
        self.args.timeout = 30
        self.args.depth = 1
        self.args.username = None
        self.args.password = None
        self.args.confluence = False
        self.args.space = None
        self.args.page_id = None
        
    @patch('src.crawler.AsyncWebCrawler')
    def test_crawler_initialization(self, mock_crawler_class):
        """Test crawler initialization."""
        crawler = Crawler(self.args)
        
        # Check that options are set correctly
        self.assertEqual(crawler.timeout, 30)
        self.assertEqual(crawler.depth, 1)
        self.assertIsNone(crawler.username)
        self.assertIsNone(crawler.password)
        self.assertFalse(crawler.is_confluence)
        
    @patch('src.crawler.AsyncWebCrawler')
    def test_crawler_with_auth(self, mock_crawler_class):
        """Test crawler with authentication."""
        # Set up args with authentication
        self.args.username = "testuser"
        self.args.password = "testpass"
        
        crawler = Crawler(self.args)
        
        # Check that auth is configured correctly
        self.assertEqual(crawler.username, "testuser")
        self.assertEqual(crawler.password, "testpass")
        self.assertIn("auth", crawler.crawler_options)
        self.assertEqual(crawler.crawler_options["auth"]["username"], "testuser")
        self.assertEqual(crawler.crawler_options["auth"]["password"], "testpass")
    
    @patch('src.crawler.AsyncWebCrawler')
    def test_crawler_with_confluence(self, mock_crawler_class):
        """Test crawler with Confluence configuration."""
        # Set up args for Confluence
        self.args.confluence = True
        self.args.space = "TEST"
        
        crawler = Crawler(self.args)
        
        # Check that Confluence options are set correctly
        self.assertTrue(crawler.is_confluence)
        self.assertEqual(crawler.space_key, "TEST")
        self.assertIn("confluence", crawler.crawler_options)
        self.assertTrue(crawler.crawler_options["confluence"])
        self.assertIn("space_key", crawler.crawler_options)
        self.assertEqual(crawler.crawler_options["space_key"], "TEST")
    
    @patch('src.crawler.AsyncWebCrawler')
    def test_extract_domain(self, mock_crawler_class):
        """Test domain extraction from URL."""
        crawler = Crawler(self.args)
        
        # Test with various URLs
        test_urls = [
            ("https://example.com", "example.com"),
            ("https://example.com/path", "example.com"),
            ("http://sub.example.com/path?query=1", "sub.example.com"),
            ("https://example.co.uk/path", "example.co.uk"),
        ]
        
        for url, expected in test_urls:
            domain = crawler.extract_domain(url)
            self.assertEqual(domain, expected)
    
    @patch('src.crawler.AsyncWebCrawler')
    async def test_crawl_single_page(self, mock_crawler_class):
        """Test crawling a single page."""
        # Set up the mock
        mock_instance = MagicMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_instance
        mock_instance.arun.return_value = {
            'title': 'Test Page',
            'url': 'https://example.com',
            'markdown': '# Test Page\n\nThis is a test page.',
            'timestamp': '2025-03-05 04:00:00'
        }
        
        crawler = Crawler(self.args)
        
        # Test crawling a single page
        result = await crawler.crawl("https://example.com")
        
        # Check the result
        self.assertEqual(result['title'], 'Test Page')
        self.assertEqual(result['url'], 'https://example.com')
        self.assertIn('markdown', result)
        
        # Verify that arun was called with the right parameters
        mock_instance.arun.assert_called_once_with(url="https://example.com")
    
    @patch('src.crawler.AsyncWebCrawler')
    async def test_crawl_with_depth(self, mock_crawler_class):
        """Test crawling with depth > 1."""
        # Set up args with depth > 1
        self.args.depth = 3
        
        # Set up the mock
        mock_instance = MagicMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_instance
        mock_instance.arun.return_value = {
            'title': 'Test Page with Depth',
            'url': 'https://example.com',
            'markdown': '# Test Page\n\nThis is a test page with depth crawling.',
            'timestamp': '2025-03-05 04:00:00'
        }
        
        crawler = Crawler(self.args)
        
        # Test crawling with depth
        result = await crawler.crawl("https://example.com")
        
        # Check the result
        self.assertEqual(result['title'], 'Test Page with Depth')
        
        # Verify that arun was called with the right parameters
        mock_instance.arun.assert_called_once_with(
            url="https://example.com",
            deep_crawl=True,
            max_pages=3
        )

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
TestCrawler.test_crawl_single_page = async_test(TestCrawler.test_crawl_single_page)
TestCrawler.test_crawl_with_depth = async_test(TestCrawler.test_crawl_with_depth)

if __name__ == '__main__':
    unittest.main()
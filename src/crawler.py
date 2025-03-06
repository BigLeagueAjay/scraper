import logging
import asyncio
import re
from typing import Dict, Any
from confluence_scraper import RobustCrawler
from crawl4ai import AsyncWebCrawler

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, args):
        self.args = args
        self.confluence_patterns = [
            re.compile(r'confluence', re.I),
            re.compile(r'atlassian\.net', re.I)
        ]

    def is_confluence_url(self, url: str) -> bool:
        return any(pattern.search(url) for pattern in self.confluence_patterns)
        
    def _extract_title_from_html(self, html: str) -> str:
        """
        Extract the title from HTML content.
        
        Args:
            html: HTML content string
            
        Returns:
            str: Extracted title or empty string if not found
        """
        if not html:
            return ""
            
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check <title> tag
            if soup.title and soup.title.string:
                return soup.title.string.strip()
            
            # Check main heading
            h1 = soup.find('h1')
            if h1 and h1.text:
                return h1.text.strip()
                
            # Check for other headings
            for heading in soup.find_all(['h2', 'h3'], limit=1):
                if heading.text:
                    return heading.text.strip()
        except Exception as e:
            logger.error(f"Error extracting title from HTML: {str(e)}")
            
        return ""

    async def crawl(self, url: str) -> Dict[str, Any]:
        if self.is_confluence_url(url):
            logger.info(f"Detected Confluence URL: {url}. Delegating to RobustCrawler.")
            robust_crawler = RobustCrawler(self.args)
            result = await robust_crawler.crawl(url)
            result['handled_by'] = 'confluence_scraper'
            return result

        # Non-Confluence fallback
        logger.info(f"Handling URL with crawl4ai: {url}")
        async with AsyncWebCrawler() as crawler:
            crawler.timeout = getattr(self.args, 'timeout', 30)
            crawler.javascript = getattr(self.args, 'render_js', True)
            crawler.wait_for = getattr(self.args, 'wait_time', 5)

            result = await crawler.arun(url=url)
            
            # Use the available attributes from CrawlResult
            # First try to use markdown, then html, then cleaned_html
            content = ""
            if hasattr(result, 'markdown') and result.markdown:
                content = str(result.markdown)
                logger.info("Using markdown content from crawl4ai")
            elif hasattr(result, 'html') and result.html:
                content = result.html
                logger.info("Using HTML content from crawl4ai")
            elif hasattr(result, 'cleaned_html') and result.cleaned_html:
                content = result.cleaned_html
                logger.info("Using cleaned HTML content from crawl4ai")
            
            # Create a result dictionary with all available information
            return {
                'content': content,
                'handled_by': 'crawl4ai',
                'url': url,
                'title': self._extract_title_from_html(result.html) if hasattr(result, 'html') and result.html else "",
                'html': result.html if hasattr(result, 'html') else "",
                'markdown': str(result.markdown) if hasattr(result, 'markdown') and result.markdown else ""
            }

# Usage example:
if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="General Web Scraper with Confluence Delegation")
    parser.add_argument('--url', required=True)
    parser.add_argument('--timeout', default=30)
    parser.add_argument('--render_js', action='store_true')
    parser.add_argument('--wait_time', default=5)
    parser.add_argument('--space', required=False)
    parser.add_argument('--page_id', required=False)

    args = parser.parse_args()

    crawler = Crawler(args)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crawler.crawl(args.url))

    print(f"Handled by {result['handled_by']}:")
    print(result['content'])

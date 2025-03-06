"""
Robust Crawler for Confluence and General Websites
"""

import os
import logging
import asyncio
from typing import Dict, Any
import urllib.parse
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
from atlassian import Confluence

logger = logging.getLogger(__name__)

class RobustCrawler:
    def __init__(self, args):
        self.args = args
        # Store URL from args if available, but it can be overridden in crawl method
        self.url = getattr(args, 'url', None)
        self.space_key = getattr(args, 'space', None)
        self.page_id = getattr(args, 'page_id', None)
        self.timeout = getattr(args, 'timeout', 60)
        self.render_js = getattr(args, 'render_js', True)
        self.wait_time = getattr(args, 'wait_time', 10)

        self.confluence_api_token = os.environ.get('CONFLUENCE_API_TOKEN')
        self.confluence_username = os.environ.get('CONFLUENCE_EMAIL')
        self.confluence = None

        # Only setup Confluence client if URL is available
        if self.url:
            self._setup_confluence_client()

    def _setup_confluence_client(self, url=None):
        # Use the provided URL or fall back to the stored URL
        confluence_url = url or self.url
        
        if not confluence_url:
            logger.warning("No URL provided for Confluence client setup.")
            return
            
        if self.confluence_api_token and self.confluence_username:
            self.confluence = Confluence(
                url=confluence_url,
                username=self.confluence_username,
                password=self.confluence_api_token
            )
            logger.info("Confluence API client configured.")
        else:
            logger.warning("Confluence API credentials missing. Falling back to HTML crawling.")

    async def crawl(self, url: str) -> Dict[str, Any]:
        # Update the URL and set up Confluence client if needed
        if url != self.url:
            self.url = url
            # If we don't have a Confluence client yet, try to set it up with the new URL
            if not self.confluence:
                self._setup_confluence_client(url)
        
        if self.confluence:
            try:
                logger.info(f"Attempting Confluence API crawl for {url}")
                page_id = self.page_id or self._extract_page_id(url)
                if not page_id:
                    logger.warning(f"No page ID found for {url}. Falling back to HTML crawling.")
                else:
                    content = self.confluence.get_page_by_id(page_id, expand='body.storage')
                    html = content['body']['storage']['value']
                    return {'content': self._html_to_markdown(html), 'source': 'confluence_api', 'url': url}
            except Exception as e:
                logger.error(f"Confluence API error: {e}. Falling back to HTML crawling.")

        # HTML fallback
        logger.info(f"Using HTML fallback for {url}")
        async with AsyncWebCrawler() as crawler:
            crawler.timeout = self.timeout
            crawler.javascript = self.render_js
            crawler.wait_for = self.wait_time

            result = await crawler.arun(url=url)
            content = self._extract_with_beautifulsoup(result.html)
            return {'content': content, 'source': 'html_fallback', 'url': url}

    def _extract_with_beautifulsoup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for unwanted in soup(["script", "style", "nav", "header", "footer"]):
            unwanted.decompose()
        main_content = soup.find("div", {"id": "main-content"}) or soup.find("article") or soup
        return main_content.get_text(separator="\n", strip=True)

    def _html_to_markdown(self, html):
        import html2text
        return html2text.html2text(html)

    def _extract_page_id(self, url):
        """
        Extract page ID from Confluence URL.
        Handles multiple Confluence URL formats:
        - ?pageId=123456 (query parameter)
        - /pages/123456 (path segment)
        - /l/cp/abcDEF123 (short link format)
        """
        logger.debug(f"Extracting page ID from URL: {url}")
        
        # Try to extract from query parameters first
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        page_id = query_params.get('pageId', [None])[0]
        
        if page_id:
            logger.debug(f"Found page ID in query parameter: {page_id}")
            return page_id
            
        # Try to extract from path
        path_parts = parsed_url.path.split('/')
        
        # Format: /wiki/spaces/SPACE/pages/123456
        if 'pages' in path_parts:
            pages_index = path_parts.index('pages')
            if pages_index < len(path_parts) - 1:
                page_id = path_parts[pages_index + 1]
                if page_id.isdigit():
                    logger.debug(f"Found page ID in path: {page_id}")
                    return page_id
        
        # Format: /display/SPACE/Page+Title?pageId=123456
        if 'display' in path_parts:
            # Already checked query params above
            pass
            
        # Format: /l/cp/abcDEF123 (short link format)
        if 'l' in path_parts and 'cp' in path_parts:
            cp_index = path_parts.index('cp')
            if cp_index < len(path_parts) - 1:
                page_id = path_parts[cp_index + 1]
                logger.debug(f"Found page ID in short link format: {page_id}")
                return page_id
                
        logger.warning(f"Could not extract page ID from URL: {url}")
        return None

# Usage example
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Robust Confluence/Web Scraper")
    parser.add_argument('--url', required=True)
    parser.add_argument('--space', required=False)
    parser.add_argument('--page_id', required=False)
    parser.add_argument('--timeout', default=60)
    parser.add_argument('--render_js', action='store_true')
    parser.add_argument('--wait_time', default=10)

    args = parser.parse_args()

    crawler = RobustCrawler(args)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crawler.crawl(args.url))

    print(f"Crawl result from {result['source']}:")
    print(result['content'])

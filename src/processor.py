"""
Content Processor module for the Web Scraper

This module handles the processing of crawled content and conversion to markdown.
"""

import os
import re
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class ContentProcessor:
    """
    Process crawled content and convert to markdown format.
    """
    
    def __init__(self):
        """
        Initialize the content processor.
        """
        logger.debug("Initializing ContentProcessor")
    
    def process(self, result: Dict[str, Any]) -> str:
        """
        Process the crawled content and convert to markdown.
        
        Args:
            result: Dictionary containing the crawl result from crawl4ai
            
        Returns:
            str: Processed markdown content
        """
        logger.info("Processing crawled content")
        
        # Initialize the content variable
        markdown_content = None
        
        # Check content sources in priority order
        if 'markdown' in result and result['markdown']:
            logger.info("Using markdown provided by crawl4ai")
            markdown_content = result['markdown']
        elif result.get('extraction_method') == 'enhanced' and result.get('content'):
            logger.info("Using enhanced extraction content")
            markdown_content = self._convert_to_markdown(result['content'])
        elif result.get('content') and result.get('content') != "Error: No content could be extracted.":
            logger.info("Using standard content")
            markdown_content = self._convert_to_markdown(result['content'])
        elif result.get('text'):
            logger.info("Using plain text content")
            markdown_content = result.get('text')
        elif result.get('html'):
            logger.info("Attempting HTML to markdown conversion")
            markdown_content = self._html_to_markdown(result.get('html'))
        
        # If still no content, log error
        if not markdown_content:
            logger.warning("No usable content found in any field")
            markdown_content = "No content could be extracted."
        
        # Extract a title if not already present in the result
        if not result.get('title') and result.get('html'):
            result['title'] = self.extract_title_from_html(result.get('html'))
        
        # Post-process the markdown to improve formatting
        processed_content = self._post_process_markdown(markdown_content, result)
        
        return processed_content
    
    def extract_title_from_html(self, html_content: str) -> str:
        """
        Extract the title from HTML content using multiple methods.
        
        Args:
            html_content: HTML content string
            
        Returns:
            str: Extracted title or empty string if not found
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Method 1: Check <title> tag
            if soup.title and soup.title.string:
                return soup.title.string.strip()
            
            # Method 2: Check Open Graph meta tags
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                return og_title['content'].strip()
            
            # Method 3: Check main heading
            h1 = soup.find('h1')
            if h1 and h1.text:
                return h1.text.strip()
            
            # Method 4: Check for other prominent headings
            for heading in soup.find_all(['h2', 'h3'], limit=1):
                if heading.text:
                    return heading.text.strip()
                    
        except Exception as e:
            logger.error(f"Error extracting title from HTML: {str(e)}")
        
        return ""
    
    def _convert_to_markdown(self, content: str) -> str:
        """
        Convert content to markdown if it contains HTML.
        
        Args:
            content: Content string that might contain HTML
            
        Returns:
            str: Markdown-formatted content
        """
        # Check if content looks like HTML
        if "<" in content and ">" in content and ("<p>" in content or "<div>" in content or "<a" in content):
            return self._html_to_markdown(content)
        return content

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to markdown.
        
        Args:
            html_content: HTML string
            
        Returns:
            str: Markdown-formatted content
        """
        logger.debug("Converting HTML to markdown")
        
        try:
            # Try using html2text if available
            try:
                import html2text
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.ignore_images = False
                h.body_width = 0  # No wrapping
                return h.handle(html_content)
            except ImportError:
                logger.warning("html2text not installed, trying BeautifulSoup")
                
            # Fall back to BeautifulSoup for basic conversion
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Simple HTML to markdown conversion
                text = soup.get_text(separator='\n\n', strip=True)
                
                return text
            except ImportError:
                logger.warning("BeautifulSoup not installed, returning raw content")
                return html_content
                
        except Exception as e:
            logger.error(f"HTML to markdown conversion failed: {str(e)}")
            return html_content  # Return original content if conversion fails
    
    def _post_process_markdown(self, markdown: str, result: Dict[str, Any]) -> str:
        """
        Perform post-processing on the markdown content.
        
        Args:
            markdown: Original markdown content
            result: Dictionary containing the crawl result
            
        Returns:
            str: Improved markdown content
        """
        logger.debug("Post-processing markdown content")
        
        # Extract title with fallback mechanisms
        title = self._extract_title(result)
        url = result.get('url', '')
        timestamp = result.get('timestamp', '')
        
        header = f"# {title}\n\n"
        metadata = f"_Source: {url}_  \n"
        if timestamp:
            metadata += f"_Crawled: {timestamp}_  \n"
        metadata += "\n---\n\n"
        
        # Combine with original content
        processed_content = header + metadata + markdown
        
        # Ensure tables are properly formatted
        processed_content = self._improve_tables(processed_content)
        
        # Fix heading levels (ensure proper hierarchy)
        processed_content = self._fix_heading_levels(processed_content)
        
        # Handle image references
        processed_content = self._process_images(processed_content)
        
        # Fix links
        processed_content = self._fix_links(processed_content)
        
        return processed_content
    
    def _extract_title(self, result: Dict[str, Any]) -> str:
        """
        Extract the title with improved fallback mechanisms.
        
        Args:
            result: Dictionary containing the crawled content
            
        Returns:
            str: Extracted title
        """
        # Try standard title field
        if result.get('title'):
            return result.get('title')
        
        # Try to extract from HTML if available
        if result.get('html'):
            title = self.extract_title_from_html(result.get('html'))
            if title:
                return title
        
        # Extract from URL if still no title
        parsed_url = urlparse(result.get('url', ''))
        path_parts = parsed_url.path.split('/')
        path_parts = [p for p in path_parts if p]
        
        if path_parts:
            # Convert last path segment to title
            last_segment = path_parts[-1]
            # Replace hyphens and underscores with spaces and capitalize
            last_segment = last_segment.replace('-', ' ').replace('_', ' ')
            if last_segment.strip():
                return ' '.join(word.capitalize() for word in last_segment.split())
        
        # Check if it's a homepage
        if not path_parts or (len(path_parts) == 1 and path_parts[0] in ('index.html', 'index.php')):
            domain = parsed_url.netloc
            return f"Home - {domain}"
        
        # Fall back to domain name
        domain = parsed_url.netloc
        return f"Documentation from {domain}"
    
    def _improve_tables(self, content: str) -> str:
        """
        Ensure tables are properly formatted in markdown.
        
        Args:
            content: Markdown content
            
        Returns:
            str: Markdown with improved table formatting
        """
        logger.debug("Improving table formatting")
        
        # Check if content contains tables
        if '|' not in content or '\n|' not in content:
            return content
            
        # Simple table alignment fix
        # Find all table sections (multiline starting with | and ending with empty line)
        table_pattern = r'(\n\|[^\n]+\|\n\|[-:| ]+\|\n(?:\|[^\n]+\|\n)+)'
        
        def format_table(match):
            table = match.group(1)
            lines = table.split('\n')
            
            # Process the table
            formatted_lines = []
            for line in lines:
                if not line:
                    continue
                
                # Skip separator line (---|---|---)
                if line.startswith('|') and all(c in '|-:' for c in line.strip('|')):
                    formatted_lines.append(line)
                    continue
                    
                # Format content lines
                if line.startswith('|') and line.endswith('|'):
                    cells = [cell.strip() for cell in line.strip('|').split('|')]
                    formatted_line = '| ' + ' | '.join(cells) + ' |'
                    formatted_lines.append(formatted_line)
                else:
                    formatted_lines.append(line)
            
            return '\n'.join(formatted_lines) + '\n'
            
        # Replace tables with formatted ones
        improved_content = re.sub(table_pattern, format_table, '\n' + content)
        
        return improved_content.lstrip('\n')
    
    def _fix_heading_levels(self, content: str) -> str:
        """
        Ensure heading levels maintain proper hierarchy.
        
        Args:
            content: Markdown content
            
        Returns:
            str: Markdown with fixed heading levels
        """
        logger.debug("Fixing heading levels")
        
        # We've already added a level 1 heading for the title,
        # so we need to ensure subsequent headings are properly nested
        
        # Split by lines to process headings
        lines = content.split('\n')
        title_done = False
        
        for i in range(len(lines)):
            # Skip the first heading (title)
            if not title_done and lines[i].startswith('# '):
                title_done = True
                continue
                
            # Process other headings: h1->h2, h2->h3, etc.
            if lines[i].startswith('#'):
                heading_level = 0
                for char in lines[i]:
                    if char == '#':
                        heading_level += 1
                    else:
                        break
                
                # Ensure no heading is higher than h2 (we've already used h1 for title)
                if heading_level == 1:
                    lines[i] = '#' + lines[i]  # h1 -> h2
                
        return '\n'.join(lines)
    
    def _process_images(self, content: str) -> str:
        """
        Process image references in the markdown.
        
        Args:
            content: Markdown content
            
        Returns:
            str: Markdown with processed image references
        """
        logger.debug("Processing image references")
        
        # Most likely already handled by crawl4ai, but we can add specific logic if needed
        return content
    
    def _fix_links(self, content: str) -> str:
        """
        Fix and normalize links in the markdown.
        
        Args:
            content: Markdown content
            
        Returns:
            str: Markdown with fixed links
        """
        logger.debug("Fixing links")
        
        # Ensure links have a space after them to prevent formatting issues
        link_pattern = r'\[(.*?)\]\((.*?)\)([^\s)])'
        fixed_content = re.sub(link_pattern, r'[\1](\2)\3', content)
        
        return fixed_content
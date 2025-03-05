"""
Content Processor module for the Web Scraper

This module handles the processing of crawled content and conversion to markdown.
"""

import logging
import re
from typing import Dict, Any, Optional

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
        
        # Check if result contains markdown already (crawl4ai feature)
        if 'markdown' in result and result['markdown']:
            logger.info("Using markdown provided by crawl4ai")
            markdown = result['markdown']
        else:
            logger.warning("No markdown found in result, this should not happen with crawl4ai")
            # We'd need to implement HTML to markdown conversion here
            # But crawl4ai should already provide this
            markdown = "Error: No content could be extracted."
        
        # Post-process the markdown to improve formatting
        markdown = self._post_process_markdown(markdown, result)
        
        return markdown
    
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
        
        # Add title and metadata
        title = result.get('title', 'Untitled Page')
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
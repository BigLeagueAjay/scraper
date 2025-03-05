"""
File Manager module for the Web Scraper

This module handles file operations such as creating directories
and saving markdown files.
"""

import os
import re
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class FileManager:
    """
    Manages file operations for the web scraper application.
    """
    
    def __init__(self, base_output_dir: Optional[str] = None):
        """
        Initialize the file manager.
        
        Args:
            base_output_dir: Base directory for saving output files
        """
        self.base_output_dir = base_output_dir or os.path.join(os.getcwd(), "scraped_content")
        logger.debug(f"Initializing FileManager with base directory: {self.base_output_dir}")
    
    def save(self, content: str, domain: str, title: str, space_key: Optional[str] = None) -> str:
        """
        Save content to a file.
        
        Args:
            content: The markdown content to save
            domain: The domain of the scraped site
            title: The title of the page
            space_key: The Confluence space key (optional)
            
        Returns:
            str: Path to the saved file
        """
        # Create the output directory structure
        output_dir = self._create_output_dir(domain, space_key)
        
        # Generate a valid filename from the title
        filename = self._generate_filename(title)
        
        # Full path to the output file
        output_path = os.path.join(output_dir, filename)
        
        # Save the content to the file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Content saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save content to {output_path}: {str(e)}")
            raise IOError(f"Failed to save content: {str(e)}")
    
    def _create_output_dir(self, domain: str, space_key: Optional[str] = None) -> str:
        """
        Create the output directory structure.
        
        Args:
            domain: The domain of the scraped site
            space_key: The Confluence space key (optional)
            
        Returns:
            str: Path to the created directory
        """
        # Clean the domain for use as a directory name
        domain_dir = self._sanitize_filename(domain)
        
        # Base path for this domain
        domain_path = os.path.join(self.base_output_dir, domain_dir)
        
        # If space_key is provided (for Confluence), create a subdirectory
        if space_key:
            space_dir = self._sanitize_filename(space_key)
            output_dir = os.path.join(domain_path, space_dir)
        else:
            output_dir = domain_path
        
        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logger.debug(f"Created output directory: {output_dir}")
        
        return output_dir
    
    def _generate_filename(self, title: str) -> str:
        """
        Generate a valid filename from the page title.
        
        Args:
            title: The title of the page
            
        Returns:
            str: A valid filename
        """
        # Sanitize the title for use as a filename
        filename = self._sanitize_filename(title)
        
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Construct final filename with extension
        return f"{filename}_{timestamp}.md"
    
    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string for use as a filename.
        
        Args:
            name: The string to sanitize
            
        Returns:
            str: A sanitized string valid for use as a filename
        """
        # Replace spaces with underscores
        sanitized = name.replace(' ', '_')
        
        # Remove invalid filename characters
        sanitized = re.sub(r'[\\/*?:"<>|]', '', sanitized)
        
        # Limit length and remove trailing periods
        sanitized = sanitized[:100].rstrip('.')
        
        # Ensure we have at least some valid characters
        if not sanitized or sanitized.isspace():
            sanitized = "unnamed"
        
        return sanitized
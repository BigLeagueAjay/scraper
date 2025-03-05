"""
Tests for the ContentProcessor module.
"""

import unittest
from src.processor import ContentProcessor

class TestContentProcessor(unittest.TestCase):
    """Test cases for the ContentProcessor class."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = ContentProcessor()
        
    def test_post_process_markdown(self):
        """Test post-processing of markdown content."""
        # Create a test result dictionary
        test_result = {
            'title': 'Test Page',
            'url': 'https://example.com/test',
            'timestamp': '2025-03-05 04:10:00'
        }
        
        # Simple markdown content
        markdown = "## Heading\n\nSome content.\n\n## Another Heading\n\n* List item 1\n* List item 2\n"
        
        # Process the markdown
        processed = self._processor_post_process_markdown(markdown, test_result)
        
        # Check that title is added
        self.assertIn("# Test Page", processed)
        
        # Check that metadata is added
        self.assertIn("_Source: https://example.com/test_", processed)
        self.assertIn("_Crawled: 2025-03-05 04:10:00_", processed)
        
        # Check that original content is preserved
        self.assertIn("## Heading", processed)
        self.assertIn("Some content.", processed)
        self.assertIn("## Another Heading", processed)
        self.assertIn("* List item 1", processed)
        self.assertIn("* List item 2", processed)
        
    def test_improve_tables(self):
        """Test table formatting improvements."""
        # Simple table in markdown
        markdown = """
## Table Example

| Column 1|Column 2|Column 3|
|---|---|---|
|Data 1|Data 2|Data 3|
|More data|More data|More data|

Some text after the table.
"""
        
        # Process the markdown
        processed = self.processor._improve_tables(markdown)
        
        # Check that table is properly formatted
        self.assertIn("| Column 1 | Column 2 | Column 3 |", processed)
        self.assertIn("| Data 1 | Data 2 | Data 3 |", processed)
        self.assertIn("| More data | More data | More data |", processed)
        
        # Check that text outside the table is preserved
        self.assertIn("## Table Example", processed)
        self.assertIn("Some text after the table.", processed)
        
    def test_fix_heading_levels(self):
        """Test fixing of heading levels."""
        # Markdown with mixed heading levels
        markdown = """# Main Title

Some intro text.

# First Section

Content of first section.

## Subsection

Content of subsection.

# Second Section

Content of second section.
"""
        
        # Process the markdown
        processed = self.processor._fix_heading_levels(markdown)
        
        # The first h1 should remain as h1
        self.assertIn("# Main Title", processed)
        
        # Subsequent h1s should be converted to h2
        self.assertIn("## First Section", processed)
        self.assertIn("## Second Section", processed)
        
        # h2 should become h3
        self.assertIn("### Subsection", processed)
        
        # Content should be preserved
        self.assertIn("Content of first section.", processed)
        self.assertIn("Content of subsection.", processed)
        self.assertIn("Content of second section.", processed)
        
    def test_fix_links(self):
        """Test fixing of links in markdown."""
        # Markdown with links
        markdown = """
Check out [Example](https://example.com)for more information.

Here's [another link](https://example.org)with the same issue.

And [one more](https://example.net) with proper spacing.
"""
        
        # Process the markdown
        processed = self.processor._fix_links(markdown)
        
        # Links should have proper spacing after them
        self.assertIn("[Example](https://example.com) for more information", processed)
        self.assertIn("[another link](https://example.org) with the same issue", processed)
        self.assertIn("[one more](https://example.net) with proper spacing", processed)
    
    def _processor_post_process_markdown(self, markdown, result):
        """
        Helper method to directly call the post-processing method.
        This is needed because the actual method is not directly exposed,
        but we want to test it specifically.
        """
        return self.processor._post_process_markdown(markdown, result)

if __name__ == '__main__':
    unittest.main()
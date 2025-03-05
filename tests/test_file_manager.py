"""
Tests for the FileManager module.
"""

import os
import unittest
import tempfile
import shutil
from src.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    """Test cases for the FileManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test output
        self.test_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(self.test_dir)
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
        
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with various inputs
        test_cases = [
            # input, expected output
            ("Simple Title", "Simple_Title"),
            ("Title with spaces!", "Title_with_spaces"),
            ("File/with\\invalid:chars?", "Filewithinvalidchars"),
            ("A" * 150, "A" * 100),  # Too long, should be truncated
            ("", "unnamed"),  # Empty string
            ("   ", "unnamed"),  # Just spaces
            ("Name.with.dots...", "Name.with.dots"),  # Trailing dots
        ]
        
        for input_name, expected in test_cases:
            result = self.file_manager._sanitize_filename(input_name)
            self.assertEqual(result, expected)
            
    def test_create_output_dir(self):
        """Test creation of output directory structure."""
        # Test regular domain
        domain = "example.com"
        output_dir = self.file_manager._create_output_dir(domain)
        expected_path = os.path.join(self.test_dir, "example.com")
        self.assertEqual(output_dir, expected_path)
        self.assertTrue(os.path.exists(expected_path))
        
        # Test with Confluence space
        space_key = "TEST"
        output_dir = self.file_manager._create_output_dir(domain, space_key)
        expected_path = os.path.join(self.test_dir, "example.com", "TEST")
        self.assertEqual(output_dir, expected_path)
        self.assertTrue(os.path.exists(expected_path))
        
    def test_generate_filename(self):
        """Test filename generation."""
        title = "Test Page"
        filename = self.file_manager._generate_filename(title)
        
        # Should be "Test_Page_TIMESTAMP.md"
        self.assertTrue(filename.startswith("Test_Page_"))
        self.assertTrue(filename.endswith(".md"))
        
    def test_save_content(self):
        """Test saving content to a file."""
        content = "# Test Content\nThis is a test."
        domain = "test-domain.com"
        title = "Test Page"
        
        output_path = self.file_manager.save(content, domain, title)
        
        # Check that the file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Check the content was saved correctly
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
            
        self.assertEqual(saved_content, content)
        
        # Check that the path follows our expected structure
        expected_dir = os.path.join(self.test_dir, "test-domain.com")
        self.assertTrue(output_path.startswith(expected_dir))
        

if __name__ == '__main__':
    unittest.main()
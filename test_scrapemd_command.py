#!/usr/bin/env python3
"""
Test script to verify the scrapemd command line tool installation.

This script checks:
1. If the 'scrapemd' command is available in PATH
2. If it returns the expected help output
3. If it can handle basic error cases properly
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return stdout, stderr, and return code."""
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True
        )
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode
    except Exception as e:
        return "", str(e), 1

def test_command_existence():
    """Test if scrapemd command exists in PATH."""
    print("Testing if 'scrapemd' command is available...")
    
    # Try to run the help command
    stdout, stderr, return_code = run_command("scrapemd --help")
    
    if return_code != 0:
        print("❌ Error: 'scrapemd' command not found in PATH")
        print(f"Error details: {stderr}")
        print("\nPossible solutions:")
        print("1. Make sure you've installed the package with: pip install -e .")
        print("2. Verify your Python scripts directory is in PATH")
        print("3. Try activating your virtual environment (if using one)")
        return False
    
    print("✅ 'scrapemd' command is available")
    return True

def test_help_output():
    """Test if the help output contains expected information."""
    print("\nTesting help output...")
    
    stdout, stderr, return_code = run_command("scrapemd --help")
    
    # Check for expected content in help
    expected_elements = [
        "--url",
        "--output",
        "--depth",
        "Authentication Options",
        "Confluence Options"
    ]
    
    all_found = True
    for element in expected_elements:
        if element not in stdout:
            print(f"❌ Expected element '{element}' not found in help output")
            all_found = False
    
    if all_found:
        print("✅ Help output contains all expected elements")
        return True
    return False

def test_error_handling():
    """Test if common errors are handled properly."""
    print("\nTesting error handling...")
    
    # Test missing URL argument
    stdout, stderr, return_code = run_command("scrapemd")
    if return_code == 0:
        print("❌ Command should fail when URL is missing")
        return False
    
    # Test invalid URL format
    stdout, stderr, return_code = run_command("scrapemd --url invalid-url")
    if return_code == 0:
        print("❌ Command should fail with invalid URL format")
        return False
    
    print("✅ Error handling works as expected")
    return True

def main():
    """Run all tests and summarize results."""
    print("=== Testing scrapemd Command Line Tool ===\n")
    
    # Run tests
    tests = [
        test_command_existence,
        test_help_output,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Print summary
    print("\n=== Test Summary ===")
    if all(results):
        print("✅ All tests passed! The scrapemd command is properly installed and working.")
        print("\nExample usage:")
        print("  scrapemd --url https://example.com")
        print("  scrapemd --url https://example.com --output ./custom_output --depth 2")
        return 0
    else:
        print(f"❌ {results.count(False)} test(s) failed. Please check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
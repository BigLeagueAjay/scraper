# Diagnostic Guide for Web Scraper

This guide provides detailed information on diagnosing and fixing common issues with the Web Scraper application.

## Common Issues and Solutions

### Import Errors

#### Issue: `ModuleNotFoundError: No module named 'src'`

This error occurs when the package is installed but the imports are not consistent with the package structure.

**Solution:**
1. Make sure you've installed the package in development mode:
   ```bash
   pip install -e .
   ```
2. If the error persists, check that the imports in your code don't use the `src.` prefix within the `src` directory itself.

#### Issue: `ModuleNotFoundError: No module named 'confluence_scraper'`

This error occurs when the package structure is not properly recognized.

**Solution:**
1. Reinstall the package:
   ```bash
   pip install -e .
   ```
2. Check that the imports in your code use the correct module names.

### Crawl4ai Issues

#### Issue: `AttributeError: 'CrawlResult' object has no attribute 'content'`

This error occurs when trying to access attributes that don't exist in the CrawlResult object from crawl4ai.

**Solution:**
1. Update to the latest version of the scraper (0.1.5 or later).
2. If you're modifying the code, use the available attributes like `result.markdown`, `result.html`, or `result.cleaned_html`.

### Authentication Issues

#### Issue: `Confluence API error: ... Falling back to HTML crawling`

This error occurs when the application can't authenticate with the Confluence API.

**Solution:**
1. Make sure you've set the correct environment variables:
   ```bash
   export CONFLUENCE_EMAIL="your.email@example.com"
   export CONFLUENCE_API_TOKEN="your-api-token"
   ```
2. Alternatively, provide the credentials directly:
   ```bash
   scrapemd --url https://confluence.example.com --username "your.email@example.com" --password "your-api-token"
   ```

### URL Detection Issues

#### Issue: Confluence URL not detected automatically

**Solution:**
1. Force Confluence mode with the `--confluence` flag:
   ```bash
   scrapemd --url https://example.atlassian.net/wiki/spaces/SPACE/pages/123456 --confluence
   ```

## Diagnostic Tools

### Logging

The application creates detailed log files in the `logs` directory. These logs contain valuable information about the crawling process, content extraction, and any errors that occurred.

To view the logs:
```bash
cat logs/scraper_TIMESTAMP.log
```

To enable verbose logging:
```bash
scrapemd --url https://example.com --verbose
```

### Test Script

The repository includes a diagnostic test script that can help identify issues with the package installation and imports:

```bash
python diagnostic_test.py
```

This script tests:
1. Import consistency
2. Confluence URL detection
3. Page ID extraction
4. Entry point configuration

## Troubleshooting Steps

If you encounter issues with the scraper, follow these steps:

1. **Check the logs**: Look at the most recent log file in the `logs` directory.
2. **Update the package**: Make sure you're using the latest version.
3. **Reinstall the package**: Run `pip install -e .` to reinstall the package.
4. **Run the diagnostic test**: Run `python diagnostic_test.py` to identify issues.
5. **Check environment variables**: Make sure any required environment variables are set.
6. **Try with verbose logging**: Run with the `--verbose` flag to get more detailed logs.

## Reporting Issues

If you've tried the troubleshooting steps and still have issues, please report them with:
1. The command you're running
2. The full error message
3. The log file contents
4. The output of `python diagnostic_test.py`
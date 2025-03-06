# Changelog

All notable changes to the Web Scraper with crawl4ai project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-03-05

### Fixed
- Package structure and import issues for better compatibility
- Entry point configuration in setup.py
- Handling of CrawlResult objects from crawl4ai
- Confluence page ID extraction to support multiple URL formats
- URL handling in RobustCrawler for more reliable operation
- Removed incorrect dependency on 'confluence_scraper' (which is a local module)

### Added
- Better fallback mechanisms for content extraction
- Enhanced error handling and logging
- Improved compatibility with different Confluence URL formats
- Better title extraction from HTML content
- Updated troubleshooting documentation

## [0.1.4] - 2025-03-05

### Added
- Deployment script (deploy.sh) for automated installation and updates
- Enhanced content extraction with multiple fallback methods
- Support for html2text and BeautifulSoup for HTML to markdown conversion
- Improved title extraction with multiple fallback mechanisms
- Documentation about deployment process and content extraction methods

### Fixed
- AttributeError when processing CrawlResult objects from crawl4ai
- Updated troubleshooting documentation to address CrawlResult-specific errors

### Changed
- Processor now handles different types of results from crawl4ai
- README.md updated with deployment information and enhanced content extraction details

## [0.1.3] - 2025-03-05

### Added
- User-friendly command-line interface with `scrapemd` command
- Proper Python package installation with setup.py
- Entry point in CLI module for easier command execution

### Changed
- Installation instructions in README.md to use pip install
- Usage examples to use the new `scrapemd` command instead of `python main.py`
- CLI module structure to support the new entry point

## [0.1.2] - 2025-03-05

### Added
- Comprehensive logging configuration documentation
- Test running instructions in README
- Table of contents for better README navigation

### Improved
- Consolidated documentation by moving content from TROUBLESHOOTING.md and CONTENT_EXPECTATIONS.md into the README
- Enhanced README structure with better organization of sections
- More detailed logging level explanations with examples
- Clear examples for running different test modules

## [0.1.1] - 2025-03-05

### Added
- Comprehensive troubleshooting documentation (TROUBLESHOOTING.md)
- Detailed guides for resolving common errors including AttributeError
- Content processing expectations documentation (CONTENT_EXPECTATIONS.md)
- Updated README.md with references to troubleshooting and content expectation guides

### Improved
- Error documentation with specific causes and solutions
- User guidance for debugging using logs
- Instructions for handling page structure issues
- Documentation of expected output structure and content processing
- Guidance for handling missing or unexpected content
- Examples of expected outputs for different page types

## [0.1.0] - 2025-03-05

### Added
- Initial project setup and architecture
- Command line interface with comprehensive arguments
- Integration with crawl4ai for web scraping
- Markdown content processing with table preservation
- Intelligent file and directory management
- Support for Confluence sites with authentication
- Configuration system with default settings
- Comprehensive error handling and logging
- Test suite with unit and integration tests
- Documentation (README, Project Plan)
- Post-installation setup utility
- PROMPT.md to track the evolution of project requirements
- PROJECT_RESOURCE_ANALYSIS.md with development metrics and API usage statistics

### Features
- Scrape web pages and convert to markdown
- Preserve table formatting in markdown output
- Organize output by domain and page title
- Support for authentication with username/password
- Special handling for Confluence sites
- Configurable crawl depth for recursive crawling
- Customizable output formatting

### Technical Details
- Asynchronous web crawling for better performance
- Modular design for easy extension
- Comprehensive logging for debugging
- Secure credential storage
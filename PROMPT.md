# Web Scraper with crawl4ai - Prompt Evolution

This document tracks the evolution of the project prompt over time, as the requirements and understanding of the project develop.

## Version 1.0.0 (2025-03-05)

### Original Prompt

```markdown
# Building a Web Scraper with crawl4ai

## Task Overview
Create a web scraping application that takes a URL as input, scrapes the content of the webpage, and converts it into a markdown file. The application should utilize the crawl4ai library (https://github.com/unclecode/crawl4ai) for the core scraping functionality.

## Technical Requirements

1. Create a command-line application that accepts a URL as an input parameter
2. Use the crawl4ai library to handle the web scraping
3. Process the scraped content and convert it to markdown format
4. Save the output as a .md file with an appropriate filename based on the webpage title or URL
5. Handle errors gracefully (invalid URLs, connection issues, etc.)
6. Include reasonable timeout settings to prevent hanging on large websites

## Implementation Steps

### Step 1: Set up the project
- Clone the crawl4ai repository: `git clone https://github.com/unclecode/crawl4ai.git`
- Install all required dependencies as specified in the repository's README
- Set up a new Python script for your application

### Step 2: Create the core scraping function
- Import the necessary modules from crawl4ai
- Implement a function that takes a URL and returns the scraped content
- Ensure proper configuration of the crawler based on crawl4ai documentation

### Step 3: Implement the markdown conversion
- Process the HTML structure of the scraped content
- Extract and maintain heading hierarchy (h1, h2, h3, etc.)
- Convert lists, tables, and other HTML elements to their markdown equivalents
- Handle images by either downloading them locally or maintaining their URLs
- Preserve links with proper markdown formatting

### Step 4: Create the command-line interface
- Parse command-line arguments to accept the URL
- Add optional arguments for customization (e.g., output path, depth of scraping)
- Implement progress reporting to show the status of the scraping operation

### Step 5: Implement file output
- Generate appropriate filenames based on page title or URL
- Save the converted markdown to the specified location
- Include metadata about the original URL and scraping date

## Example Usage
The final application should be usable with a command like:
```
python web_scraper.py --url https://example.com --output ./scraped_content/
```

## Bonus Features (Optional)
- Add support for scraping multiple pages from a website
- Implement depth control for crawling linked pages
- Add options for handling dynamic content (JavaScript-rendered pages)
- Create a simple web interface for the tool
- Add support for custom CSS selectors to target specific content

## Deliverables
- Complete Python script implementing the web scraper
- README file with installation and usage instructions
- Requirements.txt file listing all dependencies
- Sample output demonstrating the tool's capabilities

## Testing Guidelines
Test the application with various types of websites:
- Simple static pages
- Complex pages with varied content types
- News articles
- Documentation pages
- Blogs

Ensure the markdown output maintains readability and structure similar to the original webpage.
```

### Refined Prompt (Based on Implementation Experience)

```markdown
# Building a Web Scraper with crawl4ai

## Task Overview
Create a modular, extensible web scraping application that takes a URL as input, scrapes the content of the webpage, and converts it into well-formatted markdown files. The application should leverage the crawl4ai library for efficient web scraping with built-in markdown generation capabilities. The system should support authentication, handle Confluence sites specially, and organize output files in a domain-based directory structure.

## Technical Requirements

1. Create a comprehensive command-line application with support for:
   - URL input with validation
   - Authentication (username/password)
   - Confluence-specific options (space key, page ID)
   - Configurable crawl depth
   - Custom output directory
   - Timeout settings
   - Verbose logging

2. Utilize crawl4ai's AsyncWebCrawler for efficient asynchronous web scraping

3. Implement a modular architecture with:
   - Clear separation of concerns
   - Error handling and logging
   - Configuration management
   - File and directory management
   - Authentication handling
   - Content processing

4. Implement intelligent file organization:
   - Create directories based on domain names
   - Generate filenames from page titles
   - Handle Confluence spaces with nested directories
   - Include timestamps in filenames for uniqueness

5. Enhance markdown processing:
   - Preserve table structures
   - Maintain proper heading hierarchy
   - Fix link formatting
   - Include metadata about source URL and crawl date

6. Implement comprehensive error handling:
   - Handle invalid URLs
   - Manage authentication failures
   - Deal with connection issues
   - Provide meaningful error messages
   - Log detailed information for debugging

7. Add configuration system:
   - Default configuration file
   - Command line overrides
   - Support for site-specific settings

## Project Structure

```
scraper/
├── main.py                  # Main entry point
├── README.md                # Documentation
├── CHANGELOG.md             # Track changes
├── PROJECT_PLAN.md          # Architecture document
├── PROMPT.md                # This prompt evolution document
├── requirements.txt         # Dependencies
├── config/                  # Configuration files
│   └── default_config.yml   # Default settings
├── src/                     # Source code
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command line interface
│   ├── crawler.py           # Crawler implementation
│   ├── processor.py         # Content processing
│   ├── file_manager.py      # File operations
│   ├── auth_manager.py      # Authentication handling
│   ├── error_handler.py     # Error handling and logging
│   └── setup.py             # Post-installation setup
└── tests/                   # Unit and integration tests
    ├── __init__.py
    ├── test_crawler.py
    ├── test_processor.py
    ├── test_file_manager.py
    └── test_integration.py
```

## Implementation Guidelines

### CLI Module
- Implement comprehensive argument parsing with validation
- Support for required and optional parameters
- Help text and documentation
- URL validation

### Crawler Module
- Wrap AsyncWebCrawler from crawl4ai
- Configure timeout, depth, and authentication
- Special handling for Confluence sites
- Domain extraction utilities

### Content Processor
- Post-process markdown for improved formatting
- Table structure preservation
- Heading level normalization
- Link and image handling

### File Manager
- Create directory structure based on domains
- Generate unique filenames
- Special handling for Confluence spaces

### Authentication Manager
- Support for basic authentication
- Confluence-specific authentication
- Secure credential storage
- Credentials validation

### Error Handler
- Custom exception classes
- Logging configuration
- User-friendly error messages
- Debug information

### Configuration System
- Default settings in YAML format
- Command line overrides
- Configuration validation

### Setup Utility
- Post-installation configuration
- Dependency checking
- Browser installation verification

## Testing Strategy
- Unit tests for all modules
- Integration tests for end-to-end workflow
- Test with variety of websites and content types

## Example Usage
The final application should be usable with commands like:

```bash
# Basic usage
python main.py --url https://example.com

# Advanced usage
python main.py --url https://example.com --output ./custom_output --depth 2 --timeout 60

# Confluence usage
python main.py --url https://confluence.example.com --confluence --space SPACEKEY --username user --password pass
```

## Deliverables
- Complete modular Python package implementing the web scraper
- Comprehensive documentation (README, PROJECT_PLAN)
- Configuration files
- Full test suite
- Log handling

## Special Considerations
- Handle tables and complex elements properly
- Organize files by website domain in nested directories
- Include filenames with website domain plus page title
- Support authentication for Confluence with space key or page ID
- Include versioned changelog for tracking project evolution
- Add config option for crawl depth
- Comprehensive error handling with detailed logs
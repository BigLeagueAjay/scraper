# Web Scraper with crawl4ai - Project Plan

## System Architecture

The web scraper application is designed with a modular architecture to ensure maintainability, extensibility, and separation of concerns.

```
               +----------------+
               |  CLI Interface |
               +-------+--------+
                       |
         +-------------v-------------+
         |  Configuration Manager    |
         +-------------+-------------+
                       |
        +-----------------------------+
+-------+     Crawler Client          <------+
|       +-------------+---------------+      |
|                     |                      |
|       +-------------v--------------+       |
|       |     Content Processor      |       |
|       +-------------+--------------+       |
|                     |                      |
|       +-------------v--------------+       |
|       |    Markdown Converter      |       |
|       +-------------+--------------+       |
|                     |                      |
|       +-------------v--------------+       |
|       |      File Manager          |       |
+------>+----------------------------+       |
        |                                    |
        |    +----------------------+        |
        +----+ Authentication Manager+-------+
        |    +----------------------+        |
        |                                    |
        |    +----------------------+        |
        +----+    Error Handler     |        |
             +----------+-----------+        |
                        |                    |
                        v                    |
             +----------+-----------+        |
             |        Logger        +--------+
             +----------------------+
```

## Core Components

### 1. Command Line Interface
- Parse arguments (URL, output path, crawl depth, authentication)
- Support for different scraping modes (single page, recursive crawling)
- Support optional configuration file for complex setups

### 2. Configuration Manager
- Handle settings for different site types (regular websites vs Confluence)
- Store authentication credentials securely
- Configure crawler behavior (timeout, retry logic, depth)

### 3. Crawler Client
- Wrapper around crawl4ai's AsyncWebCrawler
- Configure browser settings and strategies
- Implement different crawling approaches based on site type

### 4. Content Processor
- Extract and structure the content
- Special handling for tables and other complex elements
- Clean up and normalize the extracted content

### 5. File Manager
- Create directory structure based on domain
- Generate appropriate filenames based on page titles
- Save markdown files with proper metadata

### 6. Authentication Handler
- Support for basic auth, cookies, and session management
- Special handling for Confluence authentication
- Secure storage of credentials

### 7. Error Handler & Logger
- Comprehensive error handling and retry mechanisms
- Detailed logging for troubleshooting
- Different log levels for debugging vs production

## Data Flow

1. User provides URL and options via CLI
2. CLI validates inputs and passes to Configuration Manager
3. Configuration Manager sets up the crawler with appropriate settings
4. Crawler Client fetches the webpage content
5. Content Processor extracts and structures the content
6. Markdown Converter formats the content as markdown
7. File Manager saves the markdown to the appropriate location
8. Error Handler manages exceptions throughout the process
9. Logger records the entire process for debugging and auditing

## Special Features

### Confluence Integration
- Support for Confluence-specific authentication
- Navigate space hierarchies
- Track page relationships and nesting
- Preserve space structure in output directory structure

### Table Handling
- Preserve table structure in markdown
- Handle complex tables with merged cells
- Maintain proper alignment and formatting

### Depth Control
- Configurable crawl depth for recursive crawling
- Option to stay within the same domain or sub-path
- Smart crawling to avoid duplicate content

## Project Structure

```
scraper/
├── main.py                  # Main entry point
├── README.md                # Documentation
├── PROJECT_PLAN.md          # This plan document
├── CHANGELOG.md             # Track major changes
├── requirements.txt         # Dependencies
├── config/                  # Configuration files
│   ├── default_config.yml   # Default settings
│   └── sites_config.yml     # Site-specific settings
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
    ├── __init__.py          # Test package initialization
    ├── test_crawler.py      # Crawler tests
    ├── test_processor.py    # Processor tests
    └── test_integration.py  # End-to-end tests
```

## Implementation Approach

### Phase 1: Core Functionality
1. Set up project structure and dependencies
2. Implement basic CLI with URL input
3. Create simple crawler using crawl4ai's AsyncWebCrawler
4. Implement basic markdown conversion and file saving
5. Add basic error handling

### Phase 2: Enhanced Features
1. Improve markdown conversion quality
2. Add table preservation
3. Implement directory structure based on domain/title
4. Add configurable crawl depth
5. Enhance error handling and logging

### Phase 3: Advanced Features
1. Add Confluence authentication and handling
2. Implement recursive crawling with relationship preservation
3. Add configuration file support
4. Create unit and integration tests
5. Documentation and examples

## Testing Strategy

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test interaction between components
3. **End-to-End Tests**: Test the entire application with mock websites
4. **Performance Testing**: Test with large websites to ensure reasonable performance
5. **Error Handling Tests**: Verify proper behavior with invalid inputs, network issues, etc.

## Security Considerations

1. Secure handling of authentication credentials
2. Respect robots.txt and site crawling rules
3. Implement rate limiting to avoid overloading servers
4. Secure storage of output files with sensitive content

# Web Scraper (`scrapemd`)

A powerful command-line application designed to scrape web pages and convert their contents into structured markdown files. Built upon robust scraping frameworks like **crawl4ai** and optimized for seamless Markdown conversion.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Content Processing Expectations](#content-processing-expectations)
- [Troubleshooting](#troubleshooting)
- [Logging Configuration](#logging-configuration)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Development](#development)
- [Recent Updates](#recent-updates)
- [License](#license)

---

## Features

- User-friendly CLI accepting URLs and configurable options
- High-quality Markdown conversion preserving tables and multimedia content
- Organized output based on domains, page titles, and timestamps
- Advanced handling for Confluence pages, including authentication support
- Customizable crawl depth and thorough logging
- Multiple fallback strategies for robust content extraction

---

## Installation

### Quick Start

```bash
git clone https://github.com/yourusername/scraper.git
cd scraper
pip install -e .
```

This command installs the project in editable mode and registers the `scrapemd` CLI.

### Dependency Installation

To install just dependencies:

```bash
pip install -r requirements.txt
```

### Automated Installation (Recommended)

Use the provided deployment script (`deploy.sh`) for a complete setup:

```bash
chmod +x deploy.sh
./deploy.sh
```

This script automatically:

- Creates a Python virtual environment (`.venv`)
- Installs all dependencies from `requirements.txt`
- Sets up the scraper package in editable mode
- Runs tests to verify installation
- Provides immediate access to the `scrapemd` command

---

## Usage

### Basic Usage

```bash
scrapemd --url https://example.com
```

### Advanced Usage Examples

Specify custom output directory and crawl depth:

```bash
scrapemd --url https://example.com --output ./markdown --depth 2
```

Scrape Confluence sites with authentication:

```bash
scrapemd --url https://confluence.example.com --space SPACEKEY --username user --password pass
```

---

## Configuration

Customize scraper behavior through command-line options or by modifying `config/default_config.yml`:

- Output directories
- Crawl settings (timeouts, retries, user-agent)
- Markdown formatting
- Authentication details
- Logging levels

---

## Content Processing Expectations

### Markdown Output Structure

A typical output file:

```markdown
# Page Title

_Source: https://example.com/page_  
_Crawled: 2025-03-05 05:00:00_

---

## Main Content

- Rich text, lists, and formatting
- Tables, links, and images preserved accurately

[Link text](https://example.com)

| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |
```

### Default Output Paths

- Standard sites: `./scraped_content/example.com/`
- Confluence sites: `./scraped_content/confluence.example.com/SPACEKEY/`

---

## Troubleshooting

Common solutions for frequent errors:

- **`ModuleNotFoundError`**: Run `pip install -r requirements.txt`
- **`ModuleNotFoundError: No module named 'src'`**: This can happen if the package imports are not consistent. Try reinstalling with `pip install -e .`
- **`AttributeError: 'CrawlResult' object has no attribute 'content'`**: This error has been fixed in version 0.1.5. Update to the latest version.
- **Connection issues**: Verify internet connectivity, proxies, and firewall settings
- **Timeouts**: Adjust with `--timeout` (default: 10 seconds)
- **Authentication errors**: Ensure credentials and access permissions are correct
- **Confluence URL detection issues**: The application should auto-detect Confluence URLs, but you can force Confluence mode with `--confluence`

Check logs (`logs/scraper_TIMESTAMP.log`) for detailed debugging information. The log files contain valuable information about the crawling process, content extraction, and any errors that occurred.

For more detailed troubleshooting information, see the [Diagnostic Guide](DIAGNOSTIC_GUIDE.md).

---

## Logging Configuration

Controlled via CLI and config files:

- Adjust verbosity: `--verbose`
- Configurable log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- Default logs located in `logs/`

---

## Running Tests

Execute tests easily:

```bash
python -m unittest discover tests
```

Run tests with coverage reporting:

```bash
coverage run -m unittest discover tests
coverage html
```

---

## Deployment

The automated deployment script (`deploy.sh`) performs:

- Environment setup
- Dependency installation
- Testing and validation
- Final availability checks

```bash
./deploy.sh
```

---
## Development

Refer to [PROJECT_PLAN.md](PROJECT_PLAN.md) for architecture, guidelines, and development roadmaps.

---

## Recent Updates

### Version 0.1.5 (2025-03-05)

#### Bug Fixes
- Fixed package structure and import issues for better compatibility
- Corrected entry point configuration in setup.py
- Improved handling of CrawlResult objects from crawl4ai
- Enhanced Confluence page ID extraction to support multiple URL formats
- Fixed URL handling in RobustCrawler for more reliable operation

#### Improvements
- Added better fallback mechanisms for content extraction
- Enhanced error handling and logging
- Improved compatibility with different Confluence URL formats
- Better title extraction from HTML content

#### Installation Notes
If you're upgrading from a previous version, reinstall the package with:
```bash
pip install -e .
```

---

## License

[MIT](LICENSE)
[MIT](LICENSE)

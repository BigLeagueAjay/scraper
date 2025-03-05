# Web Scraper with crawl4ai

A command-line application that takes a URL as input, scrapes the content of the webpage, and converts it into a markdown file. The application utilizes the crawl4ai library for the core scraping functionality.

## Features

- Command-line interface that accepts URLs and various options
- Converts web content into well-formatted markdown
- Preserves tables and other complex elements
- Organizes output by domain and page title
- Special handling for Confluence pages
- Configurable crawl depth
- Comprehensive error handling and logging

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/scraper.git
cd scraper
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run post-installation setup:
```
python -m src.setup
```

## Usage

Basic usage:
```
python main.py --url https://example.com
```

Additional options:
```
python main.py --url https://example.com --output ./scraped_content/ --depth 2
```

For Confluence sites:
```
python main.py --url https://confluence.example.com --space SPACEKEY --username user --password pass
```

## Configuration

You can customize the scraper behavior by editing the config files in the `config` directory or by passing command-line arguments.

## Development

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed information about the project architecture and development plan.

## License

MIT
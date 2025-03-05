#!/bin/bash
# Web Scraper Project Redeployment Script
# This script updates the Python package and restarts any necessary services

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
PROJECT_NAME="scraper"
PROJECT_DIR="$HOME/Dev/scraper"
VENV_DIR="$PROJECT_DIR/.venv"
BACKUP_DIR="$HOME/Dev/backups"
LOG_FILE="$HOME/Dev/deploy.log"

# Function to log messages
log() {
    local message="$1"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Start deployment
log "Starting deployment for $PROJECT_NAME"

# Navigate to project directory
log "Changing to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Create backup of current code
BACKUP_TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
BACKUP_FILENAME="$BACKUP_DIR/${PROJECT_NAME}_backup_$BACKUP_TIMESTAMP.tar.gz"
log "Creating backup at $BACKUP_FILENAME"
tar -czf "$BACKUP_FILENAME" --exclude=".venv" --exclude="logs" --exclude="scraped_content" .

# Check for virtual environment and create if needed
log "Checking virtual environment"
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    log "Virtual environment not found or incomplete. Creating new virtual environment."
    
    # Remove partial virtual environment if it exists
    if [ -d "$VENV_DIR" ]; then
        log "Removing existing incomplete virtual environment"
        rm -rf "$VENV_DIR"
    fi
    
    # Create new virtual environment
    log "Creating new Python virtual environment"
    python3 -m venv "$VENV_DIR"
    
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        log "ERROR: Failed to create virtual environment. Please check Python installation."
        exit 1
    fi
    
    log "Virtual environment created successfully"
else
    log "Existing virtual environment found"
fi

# Activate virtual environment
log "Activating virtual environment"
source "$VENV_DIR/bin/activate"

# Verify activation
if [ "$VIRTUAL_ENV" != "$VENV_DIR" ]; then
    log "ERROR: Virtual environment activation failed"
    exit 1
fi

# Update pip and setuptools
log "Updating pip and setuptools"
pip install --upgrade pip setuptools wheel

# Update dependencies
log "Updating dependencies"
pip install -r requirements.txt

# Add the html2text dependency if not already in requirements
if ! grep -q "html2text" requirements.txt; then
    log "Adding html2text dependency"
    pip install html2text
    echo "html2text>=2020.1.16" >> requirements.txt
fi

# Check if BeautifulSoup is installed, install if not
if ! pip show beautifulsoup4 > /dev/null 2>&1; then
    log "Installing BeautifulSoup"
    pip install beautifulsoup4
    echo "beautifulsoup4>=4.11.0" >> requirements.txt
fi

# Install the package in development mode
log "Installing package in development mode"
pip install -e .

# Run tests if they exist and pytest is installed
if [ -d "$PROJECT_DIR/tests" ]; then
    if pip show pytest > /dev/null 2>&1; then
        log "Running tests"
        python -m pytest
    else
        log "Skipping tests - pytest not installed"
    fi
fi

# Run setup
log "Running setup script"
python -m src.setup

# Clear cache files
log "Clearing Python cache files"
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Test the command
log "Testing scrapemd command"
if command -v scrapemd >/dev/null 2>&1; then
    log "scrapemd command is available"
else
    log "Warning: scrapemd command not found in path"
fi

log "Deployment completed successfully"
log "You can now use the 'scrapemd' command to test your changes"
log "Try: scrapemd --url https://docs.crawl4ai.com/"

# Deactivate virtual environment
# deactivate

echo "================================================================"
echo "Deployment completed successfully. Your code changes are now live."
echo "Run 'scrapemd --url <URL>' to test the updated scraper."
echo "================================================================"
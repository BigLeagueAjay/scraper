"""
Setup module for the Web Scraper

This module handles post-installation setup of the web scraper application.
"""

import os
import sys
import logging
import subprocess
import json
import pkg_resources
from typing import List, Dict

logger = logging.getLogger(__name__)

def check_dependencies() -> bool:
    """
    Check if all required dependencies are installed.
    
    Returns:
        bool: True if all dependencies are installed, False otherwise
    """
    required = {
        'crawl4ai': '0.5.0',
        'requests': '2.0.0',
        'keyring': '21.0.0'
    }
    
    missing = []
    
    for package, min_version in required.items():
        try:
            # Check if the package is installed
            pkg_version = pkg_resources.get_distribution(package).version
            
            # Compare versions (simplified)
            if pkg_version < min_version:
                missing.append(f"{package}>={min_version}")
                
        except pkg_resources.DistributionNotFound:
            missing.append(f"{package}>={min_version}")
    
    if missing:
        logger.warning(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    logger.info("All dependencies are installed")
    return True

def install_dependencies(dependencies: List[str]) -> bool:
    """
    Install required dependencies.
    
    Args:
        dependencies: List of dependencies to install
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    if not dependencies:
        return True
        
    logger.info(f"Installing dependencies: {', '.join(dependencies)}")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + dependencies)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def setup_config_directory() -> str:
    """
    Set up the configuration directory.
    
    Returns:
        str: Path to the configuration directory
    """
    config_dir = os.path.join(os.path.expanduser("~"), ".web_scraper")
    os.makedirs(config_dir, exist_ok=True)
    
    # Create default configuration file if it doesn't exist
    config_file = os.path.join(config_dir, "config.json")
    
    if not os.path.exists(config_file):
        default_config = {
            "output_directory": os.path.join(os.getcwd(), "scraped_content"),
            "default_timeout": 30,
            "default_depth": 1,
            "max_retries": 3,
            "respect_robots_txt": True,
            "user_agent": "Web Scraper with crawl4ai/0.1.0"
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        logger.info(f"Created default configuration at {config_file}")
    
    # Create credentials file if it doesn't exist
    creds_file = os.path.join(config_dir, "credentials.json")
    
    if not os.path.exists(creds_file):
        default_creds = {
            "sites": {}
        }
        
        with open(creds_file, 'w') as f:
            json.dump(default_creds, f, indent=2)
            
        logger.info(f"Created default credentials file at {creds_file}")
    
    return config_dir

def create_project_structure() -> None:
    """
    Create the project directory structure.
    """
    # Directories to create
    directories = [
        os.path.join(os.getcwd(), "scraped_content"),
        os.path.join(os.getcwd(), "logs")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def check_crawl4ai_installation() -> bool:
    """
    Check if crawl4ai is properly installed and configured.
    
    Returns:
        bool: True if crawl4ai is properly installed, False otherwise
    """
    try:
        # Try to import crawl4ai
        import crawl4ai
        
        # Check if browser drivers are installed
        try:
            from crawl4ai.browsers import check_browser_installation
            if not check_browser_installation():
                logger.warning("Browser installation for crawl4ai not found")
                return False
        except (ImportError, AttributeError):
            # If the function doesn't exist, we can't check
            pass
            
        logger.info("crawl4ai is properly installed")
        return True
        
    except ImportError:
        logger.error("crawl4ai is not installed")
        return False

def main():
    """
    Main setup function.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting setup for Web Scraper with crawl4ai")
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    if not dependencies_ok:
        print("Installing missing dependencies...")
        required = ['crawl4ai>=0.5.0', 'requests>=2.0.0', 'keyring>=21.0.0']
        if not install_dependencies(required):
            print("Failed to install dependencies. Please install them manually.")
            sys.exit(1)
    
    # Create config directory
    config_dir = setup_config_directory()
    print(f"Configuration directory: {config_dir}")
    
    # Create project structure
    create_project_structure()
    
    # Check crawl4ai installation
    crawl4ai_ok = check_crawl4ai_installation()
    if not crawl4ai_ok:
        print("crawl4ai is not properly installed or configured.")
        print("You may need to run the crawl4ai setup command:")
        print("  crawl4ai-setup")
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    main()
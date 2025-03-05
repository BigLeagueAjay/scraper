"""
Authentication Manager module for the Web Scraper

This module handles authentication for different types of websites,
with special focus on Confluence authentication.
"""

import logging
import base64
import json
import os
from typing import Dict, Optional, Tuple
import requests
import keyring

from src.error_handler import AuthenticationError

logger = logging.getLogger(__name__)

class AuthManager:
    """
    Manages authentication for web scraping.
    """
    
    def __init__(self):
        """
        Initialize the authentication manager.
        """
        logger.debug("Initializing AuthManager")
        
    def get_auth_for_url(self, url: str, username: Optional[str] = None, 
                         password: Optional[str] = None) -> Dict:
        """
        Get authentication configuration for a URL.
        
        Args:
            url: The URL to authenticate with
            username: Optional username override
            password: Optional password override
            
        Returns:
            Dict: Authentication configuration
        """
        logger.info(f"Getting authentication for {url}")
        
        # If username and password provided directly, use them
        if username and password:
            return self._create_auth_config(username, password)
        
        # Try to get stored credentials
        stored_username, stored_password = self._get_stored_credentials(url)
        if stored_username and stored_password:
            return self._create_auth_config(stored_username, stored_password)
        
        # No authentication available
        logger.warning(f"No authentication credentials found for {url}")
        return {}
    
    def setup_confluence_auth(self, url: str, username: str, password: str, 
                             space_key: Optional[str] = None) -> Dict:
        """
        Set up authentication for Confluence.
        
        Args:
            url: The Confluence URL
            username: Username
            password: Password
            space_key: Optional space key
            
        Returns:
            Dict: Confluence authentication configuration
        """
        logger.info(f"Setting up Confluence authentication for {url}")
        
        try:
            # Validate Confluence credentials
            if not self._validate_confluence_credentials(url, username, password):
                raise AuthenticationError(f"Invalid Confluence credentials for {url}")
            
            # Store credentials securely
            self._store_credentials(url, username, password)
            
            # Create auth config
            auth_config = self._create_auth_config(username, password)
            
            # Add Confluence-specific settings
            auth_config['confluence'] = True
            if space_key:
                auth_config['space_key'] = space_key
            
            return auth_config
            
        except Exception as e:
            logger.error(f"Failed to set up Confluence authentication: {str(e)}")
            raise AuthenticationError(f"Failed to set up Confluence authentication: {str(e)}")
    
    def _create_auth_config(self, username: str, password: str) -> Dict:
        """
        Create authentication configuration.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dict: Authentication configuration
        """
        return {
            "auth": {
                "username": username,
                "password": password
            }
        }
    
    def _validate_confluence_credentials(self, url: str, username: str, password: str) -> bool:
        """
        Validate Confluence credentials.
        
        Args:
            url: Confluence URL
            username: Username
            password: Password
            
        Returns:
            bool: True if credentials are valid
        """
        try:
            # Get base URL (without path)
            parts = url.split('/')
            base_url = '/'.join(parts[:3])  # http(s)://domain.com
            
            # Try to access Confluence REST API
            rest_url = f"{base_url}/rest/api/space"
            
            response = requests.get(
                rest_url,
                auth=(username, password),
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Confluence credentials validated successfully")
                return True
            else:
                logger.warning(f"Confluence credential validation failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error validating Confluence credentials: {str(e)}")
            return False
    
    def _store_credentials(self, url: str, username: str, password: str):
        """
        Store credentials securely.
        
        Args:
            url: The URL
            username: Username
            password: Password
        """
        try:
            # Use keyring to store the password securely
            service_name = f"web_scraper_{url}"
            keyring.set_password(service_name, username, password)
            logger.info(f"Credentials stored securely for {url}")
        except Exception as e:
            logger.warning(f"Failed to store credentials securely: {str(e)}")
            # Fall back to config file if keyring fails
            self._store_credentials_in_config(url, username, password)
    
    def _store_credentials_in_config(self, url: str, username: str, password: str):
        """
        Store credentials in config file (fallback).
        
        Args:
            url: The URL
            username: Username
            password: Password
        """
        config_dir = os.path.join(os.path.expanduser("~"), ".web_scraper")
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "credentials.json")
        
        # Load existing config if it exists
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except:
                config = {}
        else:
            config = {}
        
        # Add or update credentials
        if 'sites' not in config:
            config['sites'] = {}
            
        # Encode password in base64 (minimal security)
        encoded_password = base64.b64encode(password.encode()).decode()
        
        config['sites'][url] = {
            "username": username,
            "password": encoded_password
        }
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f)
            
        logger.info(f"Credentials stored in config file for {url}")
    
    def _get_stored_credentials(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get stored credentials for a URL.
        
        Args:
            url: The URL
            
        Returns:
            Tuple: (username, password) if found, (None, None) otherwise
        """
        try:
            # Try keyring first
            service_name = f"web_scraper_{url}"
            
            # Find username in keyring
            # (This is a simplified approach - in a real app we'd need to store usernames separately)
            username = None
            password = None
            
            # Fall back to config file
            if not username or not password:
                username, password = self._get_credentials_from_config(url)
                
            return username, password
            
        except Exception as e:
            logger.warning(f"Failed to retrieve stored credentials: {str(e)}")
            return None, None
    
    def _get_credentials_from_config(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get credentials from config file.
        
        Args:
            url: The URL
            
        Returns:
            Tuple: (username, password) if found, (None, None) otherwise
        """
        config_file = os.path.join(os.path.expanduser("~"), ".web_scraper", "credentials.json")
        
        if not os.path.exists(config_file):
            return None, None
            
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                
            if 'sites' in config and url in config['sites']:
                site_config = config['sites'][url]
                username = site_config.get('username')
                encoded_password = site_config.get('password')
                
                if username and encoded_password:
                    # Decode base64 password
                    password = base64.b64decode(encoded_password.encode()).decode()
                    return username, password
                    
        except Exception as e:
            logger.warning(f"Failed to retrieve credentials from config: {str(e)}")
            
        return None, None
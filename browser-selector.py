#!/usr/bin/python3

import sys
import subprocess
import re
import json
import logging
from pathlib import Path

# Add this directory to PATH temporarily if not already present in user session
import os
os.environ["PATH"] = f"{os.environ['HOME']}/.local/bin:{os.environ['PATH']}"

# Setup logging
log_file = Path.home() / "browser-selector.log"
logging.basicConfig(
    filename=str(log_file),
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    config_path = Path.home() / ".config" / "browser-selector" / "config.json"
    if not config_path.exists():
        logger.error(f"Config file not found at {config_path}")
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse config file: {e}")
        print(f"Error: Failed to parse config file: {e}", file=sys.stderr)
        return {}

def main():
    logger.debug(f"--- Starting browser-selector ---")
    logger.debug(f"Arguments: {sys.argv}")
    logger.debug(f"Environment PATH: {os.environ.get('PATH')}")
    
    if len(sys.argv) < 2:
        logger.error("No URL provided. Usage: browser-selector <url>")
        print("Usage: browser-selector <url>")
        sys.exit(1)

    # In case there are multiple arguments that should be treated as one URL, log them all.
    # We'll just take the first parameter as the URL for now, but log everything.
    url = sys.argv[1]
    logger.debug(f"Target URL: {url}")
    
    config = load_config()
    logger.debug(f"Loaded config: {config}")
    
    rules = config.get("rules", [])
    default_browser = config.get("default_browser", "firefox")

    # Check the URL against the rules
    for rule in rules:
        pattern = rule.get("pattern")
        command = rule.get("command")
        
        if pattern and command:
            if re.match(pattern, url, re.IGNORECASE):
                logger.info(f"URL matched rule pattern '{pattern}'. Executing: {command} '{url}'")
                subprocess.Popen(f"{command} '{url}'", shell=True)
                sys.exit(0)

    # If no rule matches, open with the default browser
    logger.info(f"No rules matched. Opening with default browser: {default_browser} '{url}'")
    subprocess.Popen(f"{default_browser} '{url}'", shell=True)

if __name__ == "__main__":
    main()

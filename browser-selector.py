#!/usr/bin/python3

import sys
import subprocess
import re
import json
from pathlib import Path

# Add this directory to PATH temporarily if not already present in user session
import os
os.environ["PATH"] = f"{os.environ['HOME']}/.local/bin:{os.environ['PATH']}"

def load_config():
    config_path = Path.home() / ".config" / "browser-selector" / "config.json"
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse config file: {e}", file=sys.stderr)
        return {}

def main():
    if len(sys.argv) < 2:
        print("Usage: browser-selector <url>")
        sys.exit(1)

    url = sys.argv[1]
    config = load_config()
    
    rules = config.get("rules", [])
    default_browser = config.get("default_browser", "firefox")

    # Check the URL against the rules
    for rule in rules:
        pattern = rule.get("pattern")
        command = rule.get("command")
        
        if pattern and command:
            if re.match(pattern, url):
                subprocess.Popen(f"{command} {url}", shell=True)
                sys.exit(0)

    # If no rule matches, open with the default browser
    subprocess.Popen(f"{default_browser} {url}", shell=True)

if __name__ == "__main__":
    main()

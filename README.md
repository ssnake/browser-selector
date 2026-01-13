# Browser Selector

A smart browser selector for Linux that automatically opens URLs in specific browsers or profiles based on configurable regex patterns. This is useful for separating work and personal browsing contexts (e.g., opening JIRA links in a work profile and Reddit links in a personal profile).

## Features

- **Pattern Matching**: Route URLs to specific browsers or profiles using regex patterns.
- **Default Fallback**: Define a default browser for URLs that don't match any rules.
- **Easy Installation**: Includes an installation script to set up symlinks and desktop entry integration.
- **JSON Configuration**: Simple JSON file for managing rules.

## Prerequisites

- Linux (tested on Ubuntu)
- Python 3
- `xdg-mime` (usually pre-installed on most desktop Linux distributions)

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd browser-selector
   ```

2. Run the installation script:
   ```bash
   ./install.sh
   ```
   This will:
   - Create a symlink to the script in `~/.local/bin`.
   - Create a `.desktop` file in `~/.local/share/applications`.
   - Register `browser-selector` as the default handler for `http`, `https`, and `text/html`.

3. Ensure `~/.local/bin` is in your `$PATH`.

## Configuration

The configuration file is located at `~/.config/browser-selector/config.json`.

The installation script will automatically create this file from `config.example.json` if it doesn't exist.

### Example Configuration

```json
{
    "rules": [
        {
            "pattern": "https?://(.*\\.)?github\\.com/.*",
            "command": "google-chrome-stable --profile-directory='Profile 1'"
        },
        {
            "pattern": "https?://(.*\\.)?gitlab\\.com/.*",
            "command": "google-chrome-stable --profile-directory='Profile 1'"
        },
        {
            "pattern": "https?://(.*\\.)?reddit\\.com/.*",
            "command": "google-chrome-stable --profile-directory='Profile 2'"
        }
    ],
    "default_browser": "firefox"
}
```

### Configuration Fields

- **rules**: A list of rule objects.
  - **pattern**: A regex string to match the URL. Note that backslashes needs to be escaped in JSON (e.g. `\\.` to match a literal dot).
  - **command**: The shell command to execute if the pattern matches. The URL will be appended to this command.
- **default_browser**: The command to execute if no rules match.

## Uninstall

To uninstall the browser selector and remove system integration:

```bash
./install.sh uninstall
```

**Note:** After uninstalling, you will need to manually set your default browser again through your system settings or using `update-alternatives` / `xdg-mime`.

## Troubleshooting

- **Browser not opening?**
  - Check if the script is executable: `chmod +x browser-selector.py`
  - Verify your regex patterns in `config.json`.
  - Check `~/.config/browser-selector/config.json` for valid JSON syntax.
  - Ensure the browser commands in your config are correct and exist in your `$PATH`.

- **Check logs:**
  Since the script runs from the desktop environment, you might not see stdout/stderr. Try running it manually from the terminal to debug:
  ```bash
  browser-selector https://example.com
  ```

#!/bin/bash

APP_NAME="browser-selector"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_PATH="$DIR/browser-selector.py"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/$APP_NAME.desktop"
SYMLINK_PATH="$BIN_DIR/$APP_NAME"
CONFIG_DIR="$HOME/.config/$APP_NAME"
CONFIG_FILE="$CONFIG_DIR/config.json"
EXAMPLE_CONFIG="$DIR/config.example.json"

install() {
    echo "Installing $APP_NAME..."

    # Ensure executable
    chmod +x "$SCRIPT_PATH"

    # Setup Config
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
        echo "Created configuration directory at $CONFIG_DIR"
    fi

    if [ ! -f "$CONFIG_FILE" ]; then
        if [ -f "$EXAMPLE_CONFIG" ]; then
            cp "$EXAMPLE_CONFIG" "$CONFIG_FILE"
            echo "Installed default configuration to $CONFIG_FILE"
        else
            echo "Warning: Example config not found. Please create $CONFIG_FILE manually."
        fi
    else
        echo "Configuration already exists at $CONFIG_FILE"
    fi

    # Create symlink
    mkdir -p "$BIN_DIR"
    ln -sf "$SCRIPT_PATH" "$SYMLINK_PATH"
    echo "Symlink created at $SYMLINK_PATH"

    # Create .desktop file
    mkdir -p "$DESKTOP_DIR"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Name=Browser Selector
Comment=Select browser based on URL rules
Exec=$SYMLINK_PATH %u
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=x-scheme-handler/http;x-scheme-handler/https;text/html;
EOF
    echo "Desktop file created at $DESKTOP_FILE"

    # Update desktop database
    update-desktop-database "$DESKTOP_DIR"

    # Set as default browser
    xdg-mime default "$APP_NAME.desktop" x-scheme-handler/http
    xdg-mime default "$APP_NAME.desktop" x-scheme-handler/https
    xdg-mime default "$APP_NAME.desktop" text/html

    echo "$APP_NAME installed and set as default browser handler."
}

uninstall() {
    echo "Uninstalling $APP_NAME..."

    # Remove symlink
    if [ -L "$SYMLINK_PATH" ]; then
        rm "$SYMLINK_PATH"
        echo "Removed symlink $SYMLINK_PATH"
    fi

    # Remove .desktop file
    if [ -f "$DESKTOP_FILE" ]; then
        rm "$DESKTOP_FILE"
        echo "Removed desktop file $DESKTOP_FILE"
    fi

    # Update desktop database
    update-desktop-database "$DESKTOP_DIR"

    echo "$APP_NAME uninstalled."
    echo "Note: You may need to manually set a new default browser."
}

if [ "$1" == "uninstall" ]; then
    uninstall
else
    install
fi

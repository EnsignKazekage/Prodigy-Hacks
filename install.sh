#!/usr/bin/env bash
# Prodigy Companion - Unix installer
# Usage: curl -fsSL https://raw.githubusercontent.com/EnsignKazekage/Prodigy-Hacks/main/scripts/install.sh | bash

set -e
REPO="https://github.com/EnsignKazekage/Prodigy-Hacks"
INSTALL_DIR="$HOME/.prodigy-companion-app"
BIN="/usr/local/bin/prodigy"

CYAN='\033[96m'; GREEN='\033[92m'; YELLOW='\033[93m'; GRAY='\033[90m'; BOLD='\033[1m'; R='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}  Prodigy Companion - Installer${R}"
echo -e "${GRAY}  ------------------------------${R}\n"

if ! command -v python3 &>/dev/null; then
    echo -e "${YELLOW}  Python3 not found. Install from https://python.org${R}"; exit 1
fi
echo -e "${GREEN}  OK Python found${R}"

if ! command -v git &>/dev/null; then
    echo -e "${YELLOW}  Git not found. Install git first.${R}"; exit 1
fi
echo -e "${GREEN}  OK Git found${R}"

if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR" && git pull --quiet
else
    git clone "$REPO" "$INSTALL_DIR" --quiet
fi
cd "$INSTALL_DIR"

python3 -m pip install -r requirements.txt --quiet
echo -e "${GREEN}  OK Dependencies installed${R}"

sudo tee "$BIN" > /dev/null << EOF
#!/usr/bin/env bash
exec python3 "$INSTALL_DIR/prodigy.py" "\$@"
EOF
sudo chmod +x "$BIN"

echo -e "${GREEN}  OK 'prodigy' command installed${R}\n"
echo -e "${GREEN}${BOLD}  Installation complete!${R}\n"
echo -e "  Try: ${CYAN}prodigy login --token YOUR_TOKEN${R}"
echo -e "       ${CYAN}prodigy use YOUR_CHILD_USER_ID${R}"
echo -e "       ${CYAN}prodigy week${R}\n"

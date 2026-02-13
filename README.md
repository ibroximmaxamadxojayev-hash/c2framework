# Advanced C2 Framework

A lightweight Command and Control (C2) framework written in Python and C++ for educational purposes, security research, and controlled lab environments.

This framework provides a centralized server that manages multiple remote agents and allows secure command execution, system monitoring, and real-time communication through a web interface.

---

# Features

• Multi-agent support
• Encrypted communication using XOR encryption
• Real-time web interface using Flask and Socket.IO
• Remote command execution
• Agent system information collection
• Command history tracking
• Multi-threaded agent handling
• Lightweight and fast agent executable

---

# Architecture Overview

The framework consists of two main components:

## 1. C2 Server (Python)

File:

```
c2_server.py
```

Responsibilities:

• Accept incoming agent connections
• Store agent information
• Execute commands remotely
• Provide web interface
• Manage communication with agents

Runs on:

```
Port 4444 → Agent listener
Port 5000 → Web interface
```

---

## 2. Agent (C++)

File:

```
src/main.cpp
```

Responsibilities:

• Connect to C2 server
• Send system information
• Receive and execute commands
• Return command output

Compiled to:

```
agent.exe
```

---

# Folder Structure

```
AdvancedC2Framework/
│
├── src/
│   └── main.cpp
│
├── templates/
│   └── index.html
│
├── static/
│
├── compile_agent.py
├── setup_mingw.py
├── c2_server.py
├── README.md
```

---

# Requirements

## Server Requirements

Python 3.8+

Install dependencies:

```
pip install flask flask-socketio
```

---

## Agent Compilation Requirements

MinGW-w64 compiler must be installed:

```
x86_64-w64-mingw32-g++
```

Recommended installation method:

MSYS2

Download:
https://www.msys2.org/

Install compiler:

```
pacman -S mingw-w64-x86_64-toolchain
```

---

# How to Compile Agent

Automatic method:

```
python compile_agent.py
```

Enter output file name when prompted:

Example:

```
agent.exe
```

Manual method:

```
x86_64-w64-mingw32-g++ src/main.cpp -o agent.exe -O2 -s -static -mwindows -lws2_32 -lwininet -ladvapi32 -lshell32 -liphlpapi
```

---

# How to Run C2 Server

Start server:

```
python c2_server.py
```

Output:

```
C2 Listener started on port 4444
Web Interface running on port 5000
```

Open browser:

```
http://localhost:5000
```

---

# How It Works

1. Server starts listener on port 4444
2. Agent connects to server
3. Agent sends system information
4. Server registers agent
5. User executes commands via web interface
6. Agent executes command and returns result
7. Server displays output

---

# Communication Protocol

Encryption method:

```
XOR encryption
```

Key:

```
0x42
```

Data flow:

```
Server → encrypted command → Agent
Agent → encrypted response → Server
```

---

# Example Agent Information

```
Hostname
Username
Operating System
Current Working Directory
Connection Status
```

---

# Educational Purpose

This project is intended for:

• Cybersecurity learning
• Red team lab environments
• Malware analysis education
• Network programming practice

Do not use on systems without permission.

---

# Author

Created for educational and research purposes.

---

# License

This project is for educational use only.

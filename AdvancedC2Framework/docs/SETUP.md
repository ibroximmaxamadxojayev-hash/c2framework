# C2 Framework Setup Guide

## Directory Structure

```
AdvancedC2Framework/
├── c2_server.py              # Main C2 server
├── README.md                 # Project documentation
├── config/                   # Configuration files
│   └── c2.config.json       # C2 settings
├── src/                      # Agent source code
│   ├── main.cpp
│   ├── evasion/             # Evasion techniques
│   ├── execution/           # Execution methods
│   ├── network/             # Network communication
│   ├── persistence/         # Persistence modules
│   └── utils/               # Utility functions
├── include/                  # C++ headers
├── agents/                   # Agent management
│   └── payloads/            # Compiled payloads
├── templates/               # Web interface
│   └── index.html          # Hacker-themed UI
├── static/                  # Static assets
│   ├── css/
│   ├── js/
│   └── assets/
└── docs/                    # Documentation
    └── SETUP.md
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install flask flask-socketio python-socketio
   ```

2. **Run C2 Server**
   ```bash
   python c2_server.py
   ```

3. **Access Web Interface**
   - Open browser to `http://localhost:5000`
   - Login with credentials (if configured)
   - Select agents to send commands

## Features

### Agent Capabilities
- Advanced evasion techniques (AMSI bypass, ETW disable, unhooking)
- Encrypted C2 communications
- Sandbox detection
- Shell command execution
- Registry persistence
- File operations

### Server Features
- Real-time agent management
- Interactive terminal interface
- Multi-agent command execution
- Session persistence
- Detailed logging

## Security Notes

**FOR AUTHORIZED SECURITY TESTING ONLY**

- Use in isolated test environments
- Configure encryption settings
- Implement authentication
- Monitor network activity
- Review all modifications

## Configuration

Edit `config/c2.config.json` to customize:
- Server host and port
- Encryption settings
- Database configuration
- Retry policies

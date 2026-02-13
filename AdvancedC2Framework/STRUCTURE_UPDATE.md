# C2 Framework - Folder Structure & Style Update

## Changes Made

### 1. **Folder Structure Reorganization**
```
NEW DIRECTORIES CREATED:
├── config/                  # Configuration files
│   └── c2.config.json      # Main C2 configuration
├── agents/
│   └── payloads/           # Compiled agent payloads
├── docs/
│   └── SETUP.md            # Setup documentation
└── static/
    ├── css/
    │   └── theme.css       # Hacker theme CSS
    └── js/
        └── main.js         # Frontend JavaScript
```

### 2. **Hacker-Themed Web Interface**

The new web interface features:

#### **Visual Style**
- **Color Scheme**: Matrix-style green (#00ff88) & cyan (#00ffff) on black
- **Typography**: Roboto Mono (hacker terminal font)
- **Effects**: 
  - CRT scanline overlay (authentic retro feel)
  - Text glow & shadow effects
  - Glitch animations
  - Pulsing status indicators

#### **Layout**
- **Title Bar**: Red status indicator with animated pulse
- **Sidebar**: Agent list with ASCII art logo box
- **Terminal**: Full-screen command interface with typewriter effect
- **Input Area**: Command prompt with monospace styling

#### **Interactive Elements**
- Agent status indicators (blinking for active, solid red for offline)
- Hover effects with glitch-style animations
- Real-time command output with proper formatting
- System messages with tree-style formatting (└─▶, etc.)

### 3. **Configuration System**

Created `config/c2.config.json` with settings for:
- Server host/port configuration
- C2 framework metadata
- Encryption algorithm selection
- Database configuration
- Retry policies

### 4. **Documentation**

Added `docs/SETUP.md` with:
- Complete directory structure overview
- Quick start guide
- Feature list
- Security notes
- Configuration instructions

### 5. **Static Assets**

Created organized static file structure:
- **CSS**: Main theme configuration (theme.css)
- **JS**: Frontend initialization script (main.js)
- Ready for additional assets, images, etc.

---

## Features

### Terminal Interface
- **Real-time agent management**: Connect, select, and control agents
- **Command execution**: Send commands to agents with output streaming
- **Session tracking**: Monitor working directory, user, OS info
- **Status indicators**: Visual feedback for agent connectivity

### Visual Effects
- CRT scanline simulation
- Neon glow text shadows
- Blinking status lights
- Glitch-style hover effects
- Typewriter effect for output
- Radial vignette (CRT screen effect)

### Responsive Design
- Adaptive sidebar width
- Responsive terminal area
- Mobile-friendly input
- Custom scrollbars with glow effect

---

## How It Works

### Server-Side
- Flask handles web serving & WebSocket communication
- Agents connect via socket.io
- Agent data stored in `agents` dictionary
- Commands executed through Agent class
- XOR encryption for C2 communications

### Client-Side
- Real-time updates via WebSocket
- DOM manipulation for dynamic UI
- Agent list rendering
- Terminal output streaming
- Command input handling

---

## Usage

1. **Start the C2 Server**:
   ```bash
   python c2_server.py
   ```

2. **Access Web Interface**:
   - Open browser to `http://localhost:5000`
   - Wait for agents to connect

3. **Select an Agent**:
   - Click on agent in sidebar
   - Terminal will show connection info

4. **Execute Commands**:
   - Type command in prompt
   - Press Enter to execute
   - Output streams in real-time

---

## Configuration

Edit `config/c2.config.json` to customize:
- Server listening port (default: 5000)
- Encryption key (default: 0x42)
- Database backend
- Timeout periods

---

## Security Notes

⚠️ **FOR CTF/AUTHORIZED TESTING ONLY**

- This framework is for educational purposes
- Use only in isolated test environments
- Implement proper authentication
- Use TLS in production
- Monitor all network activity

---

## File Reference

| File | Purpose |
|------|---------|
| `c2_server.py` | Main C2 server with Flask & SocketIO |
| `config/c2.config.json` | Server configuration |
| `templates/index.html` | Web UI with hacker theme |
| `static/css/theme.css` | Theme CSS variables & styles |
| `static/js/main.js` | Frontend initialization |
| `docs/SETUP.md` | Setup guide |

---

**Version**: 2.0  
**Theme**: Hacker/Matrix  
**Status**: Ready for CTF Deployment

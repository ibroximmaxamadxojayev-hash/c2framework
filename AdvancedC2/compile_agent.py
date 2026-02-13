#!/usr/bin/env python3
"""
C2 Agent Compiler - Automated build tool
Compiles main.cpp to Windows .exe using MinGW x86_64
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Configuration
COMPILER = "x86_64-w64-mingw32-g++"
SOURCE_FILE = "src/main.cpp"
DEFAULT_OUTPUT = "agent.exe"
OPTIMIZATION = "-O2"
STRIP_SYMBOLS = "-s"
LINK_STATIC = "-static"
WINDOWS_MODE = "-mwindows"
LIBRARIES = ["-lws2_32", "-lwininet", "-ladvapi32", "-lshell32", "-liphlpapi"]

def check_compiler():
    """Check if MinGW compiler is available"""
    try:
        result = subprocess.run([COMPILER, "--version"], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"[+] Compiler found: {COMPILER}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print(f"[-] Compiler not found: {COMPILER}")
    return False

def compile_agent(output_file=DEFAULT_OUTPUT, verbose=False):
    """
    Compile main.cpp to Windows executable
    
    Args:
        output_file (str): Output .exe filename
        verbose (bool): Show detailed compilation info
    
    Returns:
        bool: True if compilation successful, False otherwise
    """
    
    # Validate paths
    if not os.path.exists(SOURCE_FILE):
        print(f"[-] Source file not found: {SOURCE_FILE}")
        return False
    
    if not output_file.lower().endswith('.exe'):
        output_file += '.exe'
    
    # Build compiler command
    cmd = [
        COMPILER,
        SOURCE_FILE,
        "-o", output_file,
        OPTIMIZATION,
        STRIP_SYMBOLS,
        LINK_STATIC,
        WINDOWS_MODE,
    ] + LIBRARIES
    
    print(f"\n[*] Compilation Settings:")
    print(f"    Source: {SOURCE_FILE}")
    print(f"    Output: {output_file}")
    print(f"    Compiler: {COMPILER}")
    print(f"    Optimization: {OPTIMIZATION}")
    print(f"    Static linking: {LINK_STATIC}")
    print(f"    No console: {WINDOWS_MODE}")
    print(f"\n[*] Building agent...")
    
    if verbose:
        print(f"[*] Command: {' '.join(cmd)}\n")
    
    try:
        # Run compilation
        result = subprocess.run(cmd, 
                              capture_output=not verbose,
                              timeout=120)
        
        if result.returncode == 0:
            # Check if output file was created
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"[+] Compilation successful!")
                print(f"[+] Output: {output_file}")
                print(f"[+] Size: {file_size:,} bytes")
                return True
            else:
                print(f"[-] Compilation finished but .exe file not created")
                return False
        else:
            print(f"[-] Compilation failed with exit code: {result.returncode}")
            if result.stderr:
                print(f"[-] Error output:\n{result.stderr.decode('utf-8', errors='ignore')}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[-] Compilation timed out (>120s)")
        return False
    except Exception as e:
        print(f"[-] Compilation error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='C2 Agent Compiler - Compile main.cpp to Windows .exe'
    )
    parser.add_argument('-o', '--output', 
                       default=DEFAULT_OUTPUT,
                       help=f'Output filename (default: {DEFAULT_OUTPUT})')
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Show detailed compilation output')
    
    args = parser.parse_args()
    
    print("""
    ╔════════════════════════════════════════╗
    ║     C2 AGENT COMPILER v1.0            ║
    ║  Advanced Framework Build System       ║
    ╚════════════════════════════════════════╝
    """)
    
    # Check compiler availability
    if not check_compiler():
        print("\n[!] MinGW not installed. Install with:")
        print("    apt-get install mingw-w64 (Linux)")
        print("    Or: pacman -S mingw-w64-toolchain (MSYS2)")
        return 1
    
    # Compile
    success = compile_agent(args.output, args.verbose)
    
    if success:
        print(f"\n[+] Agent ready: {args.output}")
        print(f"[*] Start C2 server: python c2_server.py")
        print(f"[*] Run agent on Windows target")
        return 0
    else:
        print(f"\n[-] Build failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

COMPILER = "x86_64-w64-mingw32-g++"
SOURCE = "src/main.cpp"

FLAGS = [
    "-O2",
    "-s",
    "-static",
    "-mwindows",
    "-lws2_32",
    "-lwininet",
    "-ladvapi32",
    "-lshell32",
    "-liphlpapi"
]

def print_banner():
    print("""
╔════════════════════════════════════════╗
║        C2 AGENT COMPILER v2.0         ║
║        Automatic Build System         ║
╚════════════════════════════════════════╝
""")

def check_compiler():
    path = shutil.which(COMPILER)
    if path:
        print(f"[+] Compiler found: {path}")
        return True
    else:
        print(f"[-] Compiler not found: {COMPILER}")
        print("[!] Install MinGW and add to PATH")
        return False

def get_output_name():
    name = input("\nEnter output file name (without .exe): ").strip()
    
    if not name:
        name = "agent"
    
    if not name.endswith(".exe"):
        name += ".exe"
    
    return name

def compile_agent(output):
    
    if not Path(SOURCE).exists():
        print(f"[-] Source file not found: {SOURCE}")
        return False
    
    cmd = [COMPILER, SOURCE, "-o", output] + FLAGS
    
    print("\n[*] Compiling...")
    print("[*] Command:", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n[+] SUCCESS! Agent created: {output}")
            print(f"[+] Location: {os.path.abspath(output)}")
            return True
        else:
            print("\n[-] Compilation failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n[-] Error: {e}")
        return False

def main():
    
    print_banner()
    
    if not check_compiler():
        return
    
    output = get_output_name()
    
    compile_agent(output)

if __name__ == "__main__":
    main()


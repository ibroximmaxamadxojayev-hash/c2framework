// C2 Framework Frontend - Main Script
// Handles WebSocket communication and UI updates

const C2Framework = {
    init() {
        this.socket = io();
        this.agents = {};
        this.activeAgent = null;
        this.setupListeners();
    },

    setupListeners() {
        this.socket.on('agent_list', (agents) => this.handleAgentList(agents));
        this.socket.on('agent_connected', (agent) => this.handleAgentConnected(agent));
        this.socket.on('agent_disconnected', (data) => this.handleAgentDisconnected(data));
        this.socket.on('command_result', (data) => this.handleCommandResult(data));
    },

    handleAgentList(agentList) {
        agentList.forEach(agent => {
            this.agents[agent.id] = agent;
        });
    },

    handleAgentConnected(agent) {
        this.agents[agent.id] = agent;
    },

    handleAgentDisconnected(data) {
        if (this.agents[data.id]) {
            this.agents[data.id].status = 'Disconnected';
        }
    },

    handleCommandResult(data) {
        console.log('Command result:', data);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    C2Framework.init();
});

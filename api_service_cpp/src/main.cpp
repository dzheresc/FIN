#include "api_service/server.hpp"
#include <iostream>
#include <csignal>

static api_service::ApiServer* g_server = nullptr;

void signal_handler(int signal) {
    if (g_server) {
        std::cout << "\nShutting down server..." << std::endl;
        g_server->stop();
    }
    exit(signal);
}

int main(int argc, char* argv[]) {
    int port = 5000;
    
    if (argc > 1) {
        port = std::stoi(argv[1]);
    }
    
    api_service::ApiServer server(port);
    g_server = &server;
    
    // Setup signal handlers
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    std::cout << "Starting Financial Risk Evaluation API Server on port " << port << std::endl;
    
    int result = server.start();
    
    return result;
}


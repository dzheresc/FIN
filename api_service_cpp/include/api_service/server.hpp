#ifndef API_SERVICE_SERVER_HPP
#define API_SERVICE_SERVER_HPP

#include "risk_core/models.hpp"
#include "risk_core/json_parser.hpp"
#include "batch_processor/processor.hpp"
#include <string>
#include <memory>
#include <functional>

namespace api_service {

/**
 * HTTP server for risk evaluation API.
 */
class ApiServer {
public:
    ApiServer(int port = 5000);
    ~ApiServer();
    
    /**
     * Start the server.
     * @return 0 on success, non-zero on error
     */
    int start();
    
    /**
     * Stop the server.
     */
    void stop();
    
    /**
     * Check if server is running.
     */
    bool is_running() const { return running_; }

private:
    void setup_routes();
    std::string handle_evaluate(const std::string& request_body);
    std::string handle_batch_evaluate(const std::string& request_body);
    std::string handle_get_run(const std::string& run_id);
    std::string handle_list_runs(const std::string& query_params);
    std::string handle_health();
    
    std::string create_error_response(const std::string& code, const std::string& message);
    std::string create_success_response(const std::string& data);
    
    int port_;
    bool running_;
    std::unique_ptr<void, std::function<void(void*)>> server_; // Opaque server pointer
};

} // namespace api_service

#endif // API_SERVICE_SERVER_HPP


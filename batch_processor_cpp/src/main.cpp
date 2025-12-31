#include "batch_processor/processor.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] 
                  << " <portfolio.json> <scenarios.json> <output.csv> [--base-currency USD]" << std::endl;
        return 1;
    }
    
    std::string portfolio_file = argv[1];
    std::string scenarios_file = argv[2];
    std::string output_file = argv[3];
    std::string base_currency = "USD";
    
    // Parse optional base currency
    for (int i = 4; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--base-currency" && i + 1 < argc) {
            base_currency = argv[++i];
        }
    }
    
    try {
        batch_processor::BatchProcessor processor(base_currency);
        std::string run_id = processor.process(portfolio_file, scenarios_file, output_file);
        
        std::cout << "Processing completed successfully. Run ID: " << run_id << std::endl;
        std::cout << "Results written to: " << output_file << std::endl;
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}


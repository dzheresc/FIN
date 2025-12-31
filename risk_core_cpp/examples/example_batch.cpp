#include "risk_core/json_parser.hpp"
#include "risk_core/portfolio.hpp"
#include "risk_core/scenario.hpp"
#include "risk_core/currency.hpp"
#include "risk_core/calculations.hpp"
#include "risk_core/validators.hpp"
#include <iostream>
#include <iomanip>
#include <vector>

using namespace risk_core;

int main() {
    std::cout << "============================================================" << std::endl;
    std::cout << "Financial Risk Evaluation System - C++ Batch Processing" << std::endl;
    std::cout << "============================================================" << std::endl;
    std::cout << std::endl;
    
    try {
        // Step 1: Load portfolio from JSON file
        std::cout << "Step 1: Loading portfolio from JSON file..." << std::endl;
        Portfolio portfolio;
        if (!JsonParser::ParsePortfolio("../../tests/fixtures/sample_portfolio.json", portfolio)) {
            std::cerr << "Failed to parse portfolio JSON" << std::endl;
            return 1;
        }
        
        std::cout << "  ✓ Loaded portfolio: " << portfolio.portfolio_id() << std::endl;
        std::cout << "  ✓ Number of assets: " << portfolio.assets().size() << std::endl;
        
        // Display portfolio composition
        PortfolioManager portfolio_manager(portfolio);
        auto breakdown = portfolio_manager.currency_breakdown();
        std::cout << "  Portfolio composition:" << std::endl;
        for (const auto& pair : breakdown) {
            std::cout << "    - " << pair.first << ": " 
                      << std::fixed << std::setprecision(2) << pair.second << std::endl;
        }
        std::cout << std::endl;
        
        // Step 2: Load scenarios from JSON file
        std::cout << "Step 2: Loading scenarios from JSON file..." << std::endl;
        std::vector<Scenario> scenarios;
        if (!JsonParser::ParseScenarios("../../tests/fixtures/sample_scenarios.json", scenarios)) {
            std::cerr << "Failed to parse scenarios JSON" << std::endl;
            return 1;
        }
        
        std::cout << "  ✓ Loaded " << scenarios.size() << " scenario(s)" << std::endl;
        for (const auto& scenario : scenarios) {
            std::cout << "    - " << scenario.scenario_id() << ": " 
                      << scenario.scenario_name() << std::endl;
        }
        std::cout << std::endl;
        
        // Step 3: Apply scenario manually (for demonstration)
        if (!scenarios.empty()) {
            std::cout << "Step 3: Applying scenario manually (for demonstration)..." << std::endl;
            const Scenario& scenario = scenarios[0];
            std::cout << "  Applying scenario: " << scenario.scenario_name() << std::endl;
            std::cout << "    Market movement: " << scenario.market_movement_bps() 
                      << " bps (" << (scenario.market_movement_bps() / 100.0) << "%)" << std::endl;
            std::cout << "    Volatility change: " << scenario.volatility_change_bps() << " bps" << std::endl;
            
            ScenarioApplicator applicator(scenario);
            std::cout << "  Asset adjustments:" << std::endl;
            
            for (const auto& asset : portfolio.assets()) {
                double base_value = asset.value();
                double adjusted_value = applicator.apply_to_asset(asset, "USD");
                double change = adjusted_value - base_value;
                double change_pct = calculate_value_change_percent(base_value, adjusted_value);
                
                std::cout << "    " << asset.id() << " (" << asset.currency() << "): "
                          << std::fixed << std::setprecision(2) << base_value
                          << " → " << adjusted_value
                          << " (" << std::showpos << change << std::noshowpos
                          << ", " << std::showpos << change_pct << std::noshowpos << "%)" << std::endl;
            }
            std::cout << std::endl;
        }
        
        // Step 4: Calculate portfolio totals
        std::cout << "Step 4: Calculating portfolio totals..." << std::endl;
        double base_total = portfolio_manager.total_value("USD");
        std::cout << "  Base portfolio value (USD): " 
                  << std::fixed << std::setprecision(2) << base_total << std::endl;
        
        if (!scenarios.empty()) {
            ScenarioApplicator applicator(scenarios[0]);
            double adjusted_total = 0.0;
            for (const auto& asset : portfolio.assets()) {
                adjusted_total += applicator.apply_to_asset(asset, "USD");
            }
            double change = adjusted_total - base_total;
            double change_pct = calculate_value_change_percent(base_total, adjusted_total);
            
            std::cout << "  Adjusted portfolio value (USD): " << adjusted_total << std::endl;
            std::cout << "  Change: " << std::showpos << change << std::noshowpos
                      << " (" << std::showpos << change_pct << std::noshowpos << "%)" << std::endl;
        }
        std::cout << std::endl;
        
        std::cout << "============================================================" << std::endl;
        std::cout << "Example completed successfully!" << std::endl;
        std::cout << "============================================================" << std::endl;
        
    } catch (const ValidationError& e) {
        std::cerr << "Validation error: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}


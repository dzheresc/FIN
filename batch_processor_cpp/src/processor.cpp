#include "batch_processor/processor.hpp"
#include "batch_processor/csv_writer.hpp"
#include "risk_core/scenario.hpp"
#include <sstream>
#include <iomanip>
#include <random>
#include <chrono>
#include <stdexcept>
#include <map>

namespace batch_processor {

BatchProcessor::BatchProcessor(const std::string& base_currency)
    : base_currency_(base_currency),
      currency_converter_(std::make_unique<risk_core::CurrencyConverter>()) {
}

std::string BatchProcessor::process(
    const std::string& portfolio_file,
    const std::string& scenarios_file,
    const std::string& output_file
) {
    std::string run_id = generate_uuid();
    std::string timestamp = get_current_timestamp();
    
    // Read portfolio
    risk_core::Portfolio portfolio;
    if (!risk_core::JsonParser::ParsePortfolio(portfolio_file, portfolio)) {
        throw std::runtime_error("Failed to parse portfolio file: " + portfolio_file);
    }
    
    // Read scenarios
    std::vector<risk_core::Scenario> scenarios;
    if (!risk_core::JsonParser::ParseScenarios(scenarios_file, scenarios)) {
        throw std::runtime_error("Failed to parse scenarios file: " + scenarios_file);
    }
    
    // Process each scenario
    std::vector<risk_core::PortfolioResult> results;
    for (const auto& scenario : scenarios) {
        auto result = evaluate_portfolio(portfolio, scenario, run_id, timestamp);
        results.push_back(result);
    }
    
    // Write CSV output
    CsvWriter writer;
    writer.write_results(results, portfolio, scenarios, output_file);
    
    return run_id;
}

risk_core::PortfolioResult BatchProcessor::evaluate_portfolio(
    const risk_core::Portfolio& portfolio,
    const risk_core::Scenario& scenario,
    const std::string& run_id,
    const std::string& timestamp
) {
    // Calculate base portfolio value
    risk_core::PortfolioManager portfolio_manager(portfolio);
    auto base_breakdown = portfolio_manager.currency_breakdown();
    
    // Convert to base currency
    double base_portfolio_value = 0.0;
    for (const auto& pair : base_breakdown) {
        if (pair.first == base_currency_) {
            base_portfolio_value += pair.second;
        } else {
            double converted = currency_converter_->convert(
                pair.second, pair.first, base_currency_
            );
            base_portfolio_value += converted;
        }
    }
    
    // Apply scenario
    risk_core::ScenarioApplicator applicator(scenario);
    auto adjusted_values = applicator.apply_to_portfolio(portfolio, base_currency_);
    
    // Calculate adjusted portfolio value
    double adjusted_portfolio_value = 0.0;
    std::map<std::string, std::map<std::string, double>> currency_breakdown;
    
    for (const auto& asset : portfolio.assets()) {
        double adjusted_value = adjusted_values.at(asset.id());
        adjusted_portfolio_value += adjusted_value;
        
        // Track currency breakdown
        if (currency_breakdown.find(asset.currency()) == currency_breakdown.end()) {
            currency_breakdown[asset.currency()] = {
                {"base_value", 0.0},
                {"adjusted_value", 0.0}
            };
        }
        currency_breakdown[asset.currency()]["base_value"] += asset.value();
        currency_breakdown[asset.currency()]["adjusted_value"] += adjusted_value;
    }
    
    // Calculate changes
    double value_change = adjusted_portfolio_value - base_portfolio_value;
    double value_change_percent = risk_core::calculate_value_change_percent(
        base_portfolio_value, adjusted_portfolio_value
    );
    
    // Build result
    risk_core::PortfolioResult result;
    result.set_run_id(run_id);
    result.set_timestamp(timestamp);
    result.set_portfolio_id(portfolio.portfolio_id());
    result.set_scenario_id(scenario.scenario_id());
    result.set_base_portfolio_value(base_portfolio_value);
    result.set_adjusted_portfolio_value(adjusted_portfolio_value);
    result.set_value_change(value_change);
    result.set_value_change_percent(value_change_percent);
    result.currency_breakdown() = currency_breakdown;
    
    return result;
}

std::string BatchProcessor::generate_uuid() {
    // Simple UUID v4 generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 15);
    std::uniform_int_distribution<> dis2(8, 11);
    
    std::stringstream ss;
    ss << std::hex;
    for (int i = 0; i < 8; i++) {
        ss << dis(gen);
    }
    ss << "-";
    for (int i = 0; i < 4; i++) {
        ss << dis(gen);
    }
    ss << "-4";
    for (int i = 0; i < 3; i++) {
        ss << dis(gen);
    }
    ss << "-";
    ss << dis2(gen);
    for (int i = 0; i < 3; i++) {
        ss << dis(gen);
    }
    ss << "-";
    for (int i = 0; i < 12; i++) {
        ss << dis(gen);
    }
    
    return ss.str();
}

std::string BatchProcessor::get_current_timestamp() {
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        now.time_since_epoch()
    ) % 1000;
    
    std::stringstream ss;
    ss << std::put_time(std::gmtime(&time_t), "%Y-%m-%dT%H:%M:%S");
    ss << "." << std::setfill('0') << std::setw(3) << ms.count() << "Z";
    return ss.str();
}

} // namespace batch_processor


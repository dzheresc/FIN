#include "batch_processor/csv_writer.hpp"
#include "risk_core/currency.hpp"
#include "risk_core/scenario.hpp"
#include <iomanip>
#include <sstream>
#include <stdexcept>

namespace batch_processor {

const std::vector<std::string> CsvWriter::CSV_HEADERS = {
    "run_id", "timestamp", "portfolio_id", "scenario_id",
    "asset_id", "currency", "base_value", "adjusted_value",
    "value_change", "value_change_percent", "fx_impact",
    "market_impact", "volatility_impact"
};

void CsvWriter::write_results(
    const std::vector<risk_core::PortfolioResult>& results,
    const risk_core::Portfolio& portfolio,
    const std::vector<risk_core::Scenario>& scenarios,
    const std::string& output_file
) {
    std::ofstream file(output_file);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open output file: " + output_file);
    }
    
    write_header(file);
    
    // Create scenario map for quick lookup
    std::map<std::string, const risk_core::Scenario*> scenario_map;
    for (const auto& scenario : scenarios) {
        scenario_map[scenario.scenario_id()] = &scenario;
    }
    
    // Write asset-level rows
    for (const auto& result : results) {
        const risk_core::Scenario* scenario = nullptr;
        if (!result.scenario_id().empty()) {
            auto it = scenario_map.find(result.scenario_id());
            if (it != scenario_map.end()) {
                scenario = it->second;
            }
        }
        
        // Apply scenario to get adjusted values
        if (scenario) {
            risk_core::ScenarioApplicator applicator(*scenario);
            auto adjusted_values = applicator.apply_to_portfolio(portfolio, "USD");
            
            for (const auto& asset : portfolio.assets()) {
                double adjusted_value = adjusted_values.at(asset.id());
                write_asset_row(file, result, asset, adjusted_value, *scenario);
            }
        }
    }
    
    file.close();
}

void CsvWriter::write_header(std::ofstream& file) {
    for (size_t i = 0; i < CSV_HEADERS.size(); ++i) {
        if (i > 0) file << ",";
        file << CSV_HEADERS[i];
    }
    file << "\n";
}

void CsvWriter::write_asset_row(
    std::ofstream& file,
    const risk_core::PortfolioResult& result,
    const risk_core::Asset& asset,
    double adjusted_value,
    const risk_core::Scenario& scenario
) {
    double value_change = adjusted_value - asset.value();
    double value_change_percent = risk_core::calculate_value_change_percent(
        asset.value(), adjusted_value
    );
    
    double fx_impact = calculate_fx_impact(asset, scenario, "USD");
    double market_impact = calculate_market_impact(asset, scenario);
    double volatility_impact = calculate_volatility_impact(asset, scenario);
    
    file << result.run_id() << ","
         << result.timestamp() << ","
         << result.portfolio_id() << ","
         << result.scenario_id() << ","
         << asset.id() << ","
         << asset.currency() << ","
         << std::fixed << std::setprecision(2) << asset.value() << ","
         << adjusted_value << ","
         << value_change << ","
         << value_change_percent << ","
         << fx_impact << ","
         << market_impact << ","
         << volatility_impact << "\n";
}

double CsvWriter::calculate_fx_impact(
    const risk_core::Asset& asset,
    const risk_core::Scenario& scenario,
    const std::string& base_currency
) {
    if (asset.currency() == base_currency) {
        return 0.0;
    }
    
    double rate_change_bps = scenario.get_currency_rate_change(asset.currency());
    if (rate_change_bps != 0.0) {
        return asset.value() * (rate_change_bps / 10000.0);
    }
    return 0.0;
}

double CsvWriter::calculate_market_impact(
    const risk_core::Asset& asset,
    const risk_core::Scenario& scenario
) {
    return asset.value() * (scenario.market_movement_bps() / 10000.0);
}

double CsvWriter::calculate_volatility_impact(
    const risk_core::Asset& asset,
    const risk_core::Scenario& scenario
) {
    return asset.value() * (scenario.volatility_change_bps() / 10000.0);
}

} // namespace batch_processor


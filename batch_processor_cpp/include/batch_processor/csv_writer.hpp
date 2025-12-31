#ifndef BATCH_PROCESSOR_CSV_WRITER_HPP
#define BATCH_PROCESSOR_CSV_WRITER_HPP

#include "risk_core/models.hpp"
#include <string>
#include <vector>
#include <fstream>

namespace batch_processor {

/**
 * Writes evaluation results to CSV files.
 */
class CsvWriter {
public:
    static const std::vector<std::string> CSV_HEADERS;
    
    /**
     * Write portfolio results to CSV file.
     * @param results List of PortfolioResult objects
     * @param portfolio Original portfolio
     * @param scenarios Applied scenarios
     * @param output_file Path to output CSV file
     */
    void write_results(
        const std::vector<risk_core::PortfolioResult>& results,
        const risk_core::Portfolio& portfolio,
        const std::vector<risk_core::Scenario>& scenarios,
        const std::string& output_file
    );

private:
    void write_header(std::ofstream& file);
    void write_asset_row(
        std::ofstream& file,
        const risk_core::PortfolioResult& result,
        const risk_core::Asset& asset,
        double adjusted_value,
        const risk_core::Scenario& scenario
    );
    double calculate_fx_impact(
        const risk_core::Asset& asset,
        const risk_core::Scenario& scenario,
        const std::string& base_currency
    );
    double calculate_market_impact(
        const risk_core::Asset& asset,
        const risk_core::Scenario& scenario
    );
    double calculate_volatility_impact(
        const risk_core::Asset& asset,
        const risk_core::Scenario& scenario
    );
};

} // namespace batch_processor

#endif // BATCH_PROCESSOR_CSV_WRITER_HPP

#ifndef BATCH_PROCESSOR_PROCESSOR_HPP
#define BATCH_PROCESSOR_PROCESSOR_HPP

#include "risk_core/models.hpp"
#include "risk_core/json_parser.hpp"
#include "risk_core/portfolio.hpp"
#include "risk_core/scenario.hpp"
#include "risk_core/currency.hpp"
#include "risk_core/calculations.hpp"
#include <string>
#include <vector>
#include <memory>

namespace batch_processor {

/**
 * Main processor for batch evaluation of portfolios against scenarios.
 */
class BatchProcessor {
public:
    explicit BatchProcessor(const std::string& base_currency = "USD");
    
    /**
     * Process portfolio against scenarios and generate CSV output.
     * @param portfolio_file Path to portfolio JSON file
     * @param scenarios_file Path to scenarios JSON file
     * @param output_file Path to output CSV file
     * @return Run ID (UUID) for this processing run
     * @throws std::runtime_error if processing fails
     */
    std::string process(
        const std::string& portfolio_file,
        const std::string& scenarios_file,
        const std::string& output_file
    );

private:
    risk_core::PortfolioResult evaluate_portfolio(
        const risk_core::Portfolio& portfolio,
        const risk_core::Scenario& scenario,
        const std::string& run_id,
        const std::string& timestamp
    );
    
    std::string base_currency_;
    std::unique_ptr<risk_core::CurrencyConverter> currency_converter_;
    
    std::string generate_uuid();
    std::string get_current_timestamp();
};

} // namespace batch_processor

#endif // BATCH_PROCESSOR_PROCESSOR_HPP


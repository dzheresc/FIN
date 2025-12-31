#ifndef RISK_CORE_SCENARIO_HPP
#define RISK_CORE_SCENARIO_HPP

#include "models.hpp"
#include <string>
#include <map>

namespace risk_core {

/**
 * Applies scenarios to assets and portfolios.
 */
class ScenarioApplicator {
public:
    explicit ScenarioApplicator(const Scenario& scenario) : scenario_(scenario) {}
    
    /**
     * Apply scenario to a single asset.
     * @param asset Asset to apply scenario to
     * @param base_currency Base currency for calculations
     * @return Adjusted asset value
     */
    double apply_to_asset(const Asset& asset, const std::string& base_currency) const;
    
    /**
     * Apply scenario to entire portfolio.
     * @param portfolio Portfolio to apply scenario to
     * @param base_currency Base currency for calculations
     * @return Map of asset IDs to adjusted values
     */
    std::map<std::string, double> apply_to_portfolio(
        const Portfolio& portfolio,
        const std::string& base_currency
    ) const;

private:
    double apply_market_movement(double value) const;
    double apply_volatility_adjustment(double value) const;
    double apply_currency_change(
        double value,
        const std::string& from_currency,
        const std::string& to_currency
    ) const;
    
    const Scenario& scenario_;
};

} // namespace risk_core

#endif // RISK_CORE_SCENARIO_HPP


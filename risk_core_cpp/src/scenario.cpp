#include "risk_core/scenario.hpp"
#include "risk_core/currency.hpp"
#include <cmath>

namespace risk_core {

double ScenarioApplicator::apply_to_asset(
    const Asset& asset,
    const std::string& base_currency
) const {
    double adjusted_value = asset.value();
    
    // Apply market movement
    adjusted_value = apply_market_movement(adjusted_value);
    
    // Apply volatility adjustment
    adjusted_value = apply_volatility_adjustment(adjusted_value);
    
    // Apply currency rate changes if applicable
    if (asset.currency() != base_currency) {
        adjusted_value = apply_currency_change(
            adjusted_value,
            asset.currency(),
            base_currency
        );
    }
    
    return adjusted_value;
}

std::map<std::string, double> ScenarioApplicator::apply_to_portfolio(
    const Portfolio& portfolio,
    const std::string& base_currency
) const {
    std::map<std::string, double> results;
    
    for (const auto& asset : portfolio.assets()) {
        results[asset.id()] = apply_to_asset(asset, base_currency);
    }
    
    return results;
}

double ScenarioApplicator::apply_market_movement(double value) const {
    double movement_factor = 1.0 + (scenario_.market_movement_bps() / 10000.0);
    return value * movement_factor;
}

double ScenarioApplicator::apply_volatility_adjustment(double value) const {
    double volatility_factor = 1.0 + (scenario_.volatility_change_bps() / 10000.0);
    return value * volatility_factor;
}

double ScenarioApplicator::apply_currency_change(
    double value,
    const std::string& from_currency,
    const std::string& to_currency
) const {
    // Check if currency rate change exists for from_currency
    double rate_change_bps = scenario_.get_currency_rate_change(from_currency);
    if (rate_change_bps != 0.0) {
        double rate_factor = 1.0 + (rate_change_bps / 10000.0);
        return value * rate_factor;
    }
    return value;
}

} // namespace risk_core


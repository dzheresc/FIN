#include "risk_core/validators.hpp"
#include <algorithm>
#include <cctype>

namespace risk_core {

void validate_currency_code(const std::string& currency) {
    if (currency.empty() || currency.length() != 3) {
        throw ValidationError("Invalid currency code: " + currency + ". Must be 3 characters (ISO 4217)");
    }
    
    for (char c : currency) {
        if (!std::isalpha(c) || !std::isupper(c)) {
            throw ValidationError("Invalid currency code: " + currency + ". Must be uppercase letters");
        }
    }
}

void validate_asset(const Asset& asset) {
    if (asset.id().empty()) {
        throw ValidationError("Asset ID cannot be empty");
    }
    
    validate_currency_code(asset.currency());
    
    if (asset.value() < 0.0) {
        throw ValidationError("Asset value cannot be negative: " + std::to_string(asset.value()));
    }
}

void validate_portfolio(const Portfolio& portfolio) {
    if (portfolio.assets().empty()) {
        throw ValidationError("Portfolio must contain at least one asset");
    }
    
    std::vector<std::string> asset_ids;
    for (const auto& asset : portfolio.assets()) {
        validate_asset(asset);
        
        if (std::find(asset_ids.begin(), asset_ids.end(), asset.id()) != asset_ids.end()) {
            throw ValidationError("Duplicate asset ID: " + asset.id());
        }
        asset_ids.push_back(asset.id());
    }
}

void validate_scenario(const Scenario& scenario) {
    // Validate basis points are within reasonable range
    // Typically -10000 to +10000 bps (-100% to +100%)
    const double max_bps = 10000.0;
    const double min_bps = -10000.0;
    
    if (scenario.market_movement_bps() < min_bps || scenario.market_movement_bps() > max_bps) {
        throw ValidationError("Market movement BPS out of range: " + 
                             std::to_string(scenario.market_movement_bps()) +
                             ". Must be between " + std::to_string(min_bps) + 
                             " and " + std::to_string(max_bps));
    }
    
    if (scenario.volatility_change_bps() < min_bps || scenario.volatility_change_bps() > max_bps) {
        throw ValidationError("Volatility change BPS out of range: " + 
                             std::to_string(scenario.volatility_change_bps()) +
                             ". Must be between " + std::to_string(min_bps) + 
                             " and " + std::to_string(max_bps));
    }
    
    if (scenario.interest_rate_change_bps() < min_bps || scenario.interest_rate_change_bps() > max_bps) {
        throw ValidationError("Interest rate change BPS out of range: " + 
                             std::to_string(scenario.interest_rate_change_bps()) +
                             ". Must be between " + std::to_string(min_bps) + 
                             " and " + std::to_string(max_bps));
    }
    
    // Validate currency rate changes
    for (const auto& pair : scenario.currency_rate_changes()) {
        validate_currency_code(pair.first);
        if (pair.second < min_bps || pair.second > max_bps) {
            throw ValidationError("Currency rate change BPS for " + pair.first + 
                                 " out of range: " + std::to_string(pair.second) +
                                 ". Must be between " + std::to_string(min_bps) + 
                                 " and " + std::to_string(max_bps));
        }
    }
}

} // namespace risk_core


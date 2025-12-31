#include "risk_core/portfolio.hpp"
#include "risk_core/currency.hpp"
#include <algorithm>

namespace risk_core {

double PortfolioManager::total_value(const std::string& base_currency) const {
    CurrencyConverter converter;
    double total = 0.0;
    
    for (const auto& asset : portfolio_.assets()) {
        if (asset.currency() == base_currency) {
            total += asset.value();
        } else {
            double converted = converter.convert(
                asset.value(),
                asset.currency(),
                base_currency
            );
            total += converted;
        }
    }
    
    return total;
}

std::map<std::string, double> PortfolioManager::currency_breakdown() const {
    std::map<std::string, double> breakdown;
    
    for (const auto& asset : portfolio_.assets()) {
        breakdown[asset.currency()] += asset.value();
    }
    
    return breakdown;
}

} // namespace risk_core


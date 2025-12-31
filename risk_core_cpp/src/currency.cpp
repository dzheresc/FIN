#include "risk_core/currency.hpp"
#include <algorithm>

namespace risk_core {

CurrencyConverter::CurrencyConverter() {
    initialize_default_rates();
}

void CurrencyConverter::initialize_default_rates() {
    // Default exchange rates (to USD)
    base_rates_["USD"] = 1.0;
    base_rates_["EUR"] = 1.10;
    base_rates_["GBP"] = 1.25;
    base_rates_["JPY"] = 0.0067;
    base_rates_["CHF"] = 1.12;
    base_rates_["CAD"] = 0.74;
    base_rates_["AUD"] = 0.65;
}

double CurrencyConverter::convert(
    double value,
    const std::string& from_currency,
    const std::string& to_currency,
    double rate_change_bps
) const {
    if (from_currency == to_currency) {
        return value;
    }
    
    // Get base rates
    double from_rate = 1.0;
    double to_rate = 1.0;
    
    auto from_it = base_rates_.find(from_currency);
    if (from_it != base_rates_.end()) {
        from_rate = from_it->second;
    }
    
    auto to_it = base_rates_.find(to_currency);
    if (to_it != base_rates_.end()) {
        to_rate = to_it->second;
    }
    
    // Apply rate change
    if (rate_change_bps != 0.0) {
        double rate_factor = 1.0 + (rate_change_bps / 10000.0);
        from_rate = from_rate * rate_factor;
    }
    
    // Convert: value_in_usd = value / from_rate
    // Then: value_in_target = value_in_usd * to_rate
    double value_in_usd = value / from_rate;
    double value_in_target = value_in_usd * to_rate;
    
    return value_in_target;
}

std::map<std::string, double> CurrencyConverter::get_base_rates() const {
    return base_rates_;
}

void CurrencyConverter::update_rates(const std::map<std::string, double>& new_rates) {
    for (const auto& pair : new_rates) {
        base_rates_[pair.first] = pair.second;
    }
}

} // namespace risk_core


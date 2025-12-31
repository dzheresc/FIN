#ifndef RISK_CORE_CURRENCY_HPP
#define RISK_CORE_CURRENCY_HPP

#include <string>
#include <map>

namespace risk_core {

/**
 * Handles currency conversions with rate changes.
 */
class CurrencyConverter {
public:
    CurrencyConverter();
    
    /**
     * Convert value from one currency to another with optional rate change.
     * @param value Value to convert
     * @param from_currency Source currency code (ISO 4217)
     * @param to_currency Target currency code (ISO 4217)
     * @param rate_change_bps Rate change in basis points (default: 0)
     * @return Converted value
     */
    double convert(
        double value,
        const std::string& from_currency,
        const std::string& to_currency,
        double rate_change_bps = 0.0
    ) const;
    
    /**
     * Get current base exchange rates.
     * @return Map of currency codes to exchange rates
     */
    std::map<std::string, double> get_base_rates() const;
    
    /**
     * Update base exchange rates.
     * @param new_rates Map of currency codes to new rates
     */
    void update_rates(const std::map<std::string, double>& new_rates);

private:
    std::map<std::string, double> base_rates_;
    void initialize_default_rates();
};

} // namespace risk_core

#endif // RISK_CORE_CURRENCY_HPP


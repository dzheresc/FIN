#ifndef RISK_CORE_PORTFOLIO_HPP
#define RISK_CORE_PORTFOLIO_HPP

#include "models.hpp"
#include <string>
#include <map>

namespace risk_core {

/**
 * Manages portfolio operations and calculations.
 */
class PortfolioManager {
public:
    explicit PortfolioManager(const Portfolio& portfolio) : portfolio_(portfolio) {}
    
    /**
     * Calculate total portfolio value in base currency.
     * @param base_currency Target currency code (ISO 4217)
     * @return Total value in base currency
     */
    double total_value(const std::string& base_currency) const;
    
    /**
     * Get portfolio value breakdown by currency.
     * @return Map of currency codes to total values
     */
    std::map<std::string, double> currency_breakdown() const;

private:
    const Portfolio& portfolio_;
};

} // namespace risk_core

#endif // RISK_CORE_PORTFOLIO_HPP


#ifndef RISK_CORE_CALCULATIONS_HPP
#define RISK_CORE_CALCULATIONS_HPP

#include <string>

namespace risk_core {

/**
 * Apply market movement in basis points to a value.
 * @param value Base value
 * @param movement_bps Movement in basis points (e.g., 100 = 1%)
 * @return Adjusted value
 */
double apply_market_movement(double value, double movement_bps);

/**
 * Apply volatility adjustment to a value.
 * @param value Base value
 * @param volatility_change_bps Volatility change in basis points
 * @return Adjusted value
 */
double apply_volatility_adjustment(double value, double volatility_change_bps);

/**
 * Calculate percentage change between base and adjusted values.
 * @param base_value Original value
 * @param adjusted_value Value after scenario application
 * @return Percentage change
 */
double calculate_value_change_percent(double base_value, double adjusted_value);

} // namespace risk_core

#endif // RISK_CORE_CALCULATIONS_HPP


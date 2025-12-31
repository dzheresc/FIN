#include "risk_core/calculations.hpp"
#include <cmath>

namespace risk_core {

double apply_market_movement(double value, double movement_bps) {
    double movement_factor = 1.0 + (movement_bps / 10000.0);
    return value * movement_factor;
}

double apply_volatility_adjustment(double value, double volatility_change_bps) {
    double volatility_factor = 1.0 + (volatility_change_bps / 10000.0);
    return value * volatility_factor;
}

double calculate_value_change_percent(double base_value, double adjusted_value) {
    if (base_value == 0.0) {
        return 0.0;
    }
    double change = adjusted_value - base_value;
    return (change / base_value) * 100.0;
}

} // namespace risk_core


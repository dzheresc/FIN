#ifndef RISK_CORE_VALIDATORS_HPP
#define RISK_CORE_VALIDATORS_HPP

#include "models.hpp"
#include <string>
#include <stdexcept>

namespace risk_core {

/**
 * Exception thrown when validation fails.
 */
class ValidationError : public std::runtime_error {
public:
    explicit ValidationError(const std::string& message) : std::runtime_error(message) {}
};

/**
 * Validate currency code format (ISO 4217).
 * @param currency Currency code to validate
 * @throws ValidationError if currency code is invalid
 */
void validate_currency_code(const std::string& currency);

/**
 * Validate an asset object.
 * @param asset Asset to validate
 * @throws ValidationError if asset is invalid
 */
void validate_asset(const Asset& asset);

/**
 * Validate a portfolio object.
 * @param portfolio Portfolio to validate
 * @throws ValidationError if portfolio is invalid
 */
void validate_portfolio(const Portfolio& portfolio);

/**
 * Validate a scenario object.
 * @param scenario Scenario to validate
 * @throws ValidationError if scenario is invalid
 */
void validate_scenario(const Scenario& scenario);

} // namespace risk_core

#endif // RISK_CORE_VALIDATORS_HPP


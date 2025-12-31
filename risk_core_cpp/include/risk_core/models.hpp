#ifndef RISK_CORE_MODELS_HPP
#define RISK_CORE_MODELS_HPP

#include <string>
#include <vector>
#include <map>
#include <optional>
#include <memory>

namespace risk_core {

// Forward declarations
class Asset;
class Portfolio;
class Scenario;
class PortfolioResult;

/**
 * Represents a single financial asset.
 */
class Asset {
public:
    Asset() = default;
    Asset(const std::string& id, const std::string& currency, double value)
        : id_(id), currency_(currency), value_(value) {}
    
    const std::string& id() const { return id_; }
    void set_id(const std::string& id) { id_ = id; }
    
    const std::string& currency() const { return currency_; }
    void set_currency(const std::string& currency) { currency_ = currency; }
    
    double value() const { return value_; }
    void set_value(double value) { value_ = value; }

private:
    std::string id_;
    std::string currency_;
    double value_ = 0.0;
};

/**
 * Represents a collection of assets.
 */
class Portfolio {
public:
    Portfolio() = default;
    
    const std::string& portfolio_id() const { return portfolio_id_; }
    void set_portfolio_id(const std::string& id) { portfolio_id_ = id; }
    
    const std::vector<Asset>& assets() const { return assets_; }
    std::vector<Asset>& assets() { return assets_; }
    
    void add_asset(const Asset& asset) { assets_.push_back(asset); }
    void clear_assets() { assets_.clear(); }

private:
    std::string portfolio_id_;
    std::vector<Asset> assets_;
};

/**
 * Represents a market scenario with various risk factors.
 */
class Scenario {
public:
    Scenario() = default;
    
    const std::string& scenario_id() const { return scenario_id_; }
    void set_scenario_id(const std::string& id) { scenario_id_ = id; }
    
    const std::string& scenario_name() const { return scenario_name_; }
    void set_scenario_name(const std::string& name) { scenario_name_ = name; }
    
    double market_movement_bps() const { return market_movement_bps_; }
    void set_market_movement_bps(double bps) { market_movement_bps_ = bps; }
    
    double volatility_change_bps() const { return volatility_change_bps_; }
    void set_volatility_change_bps(double bps) { volatility_change_bps_ = bps; }
    
    double interest_rate_change_bps() const { return interest_rate_change_bps_; }
    void set_interest_rate_change_bps(double bps) { interest_rate_change_bps_ = bps; }
    
    const std::map<std::string, double>& currency_rate_changes() const { return currency_rate_changes_; }
    std::map<std::string, double>& currency_rate_changes() { return currency_rate_changes_; }
    
    void set_currency_rate_change(const std::string& currency, double bps) {
        currency_rate_changes_[currency] = bps;
    }
    
    double get_currency_rate_change(const std::string& currency) const {
        auto it = currency_rate_changes_.find(currency);
        return (it != currency_rate_changes_.end()) ? it->second : 0.0;
    }

private:
    std::string scenario_id_;
    std::string scenario_name_;
    double market_movement_bps_ = 0.0;
    double volatility_change_bps_ = 0.0;
    double interest_rate_change_bps_ = 0.0;
    std::map<std::string, double> currency_rate_changes_;
};

/**
 * Results of applying a scenario to a portfolio.
 */
class PortfolioResult {
public:
    PortfolioResult() = default;
    
    const std::string& run_id() const { return run_id_; }
    void set_run_id(const std::string& id) { run_id_ = id; }
    
    const std::string& timestamp() const { return timestamp_; }
    void set_timestamp(const std::string& ts) { timestamp_ = ts; }
    
    const std::string& portfolio_id() const { return portfolio_id_; }
    void set_portfolio_id(const std::string& id) { portfolio_id_ = id; }
    
    const std::string& scenario_id() const { return scenario_id_; }
    void set_scenario_id(const std::string& id) { scenario_id_ = id; }
    
    double base_portfolio_value() const { return base_portfolio_value_; }
    void set_base_portfolio_value(double value) { base_portfolio_value_ = value; }
    
    double adjusted_portfolio_value() const { return adjusted_portfolio_value_; }
    void set_adjusted_portfolio_value(double value) { adjusted_portfolio_value_ = value; }
    
    double value_change() const { return value_change_; }
    void set_value_change(double change) { value_change_ = change; }
    
    double value_change_percent() const { return value_change_percent_; }
    void set_value_change_percent(double percent) { value_change_percent_ = percent; }
    
    const std::map<std::string, std::map<std::string, double>>& currency_breakdown() const {
        return currency_breakdown_;
    }
    std::map<std::string, std::map<std::string, double>>& currency_breakdown() {
        return currency_breakdown_;
    }

private:
    std::string run_id_;
    std::string timestamp_;
    std::string portfolio_id_;
    std::string scenario_id_;
    double base_portfolio_value_ = 0.0;
    double adjusted_portfolio_value_ = 0.0;
    double value_change_ = 0.0;
    double value_change_percent_ = 0.0;
    std::map<std::string, std::map<std::string, double>> currency_breakdown_;
};

} // namespace risk_core

#endif // RISK_CORE_MODELS_HPP


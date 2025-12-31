#ifndef RISK_CORE_JSON_PARSER_HPP
#define RISK_CORE_JSON_PARSER_HPP

#include "models.hpp"
#include <string>
#include <memory>
#include <vector>

namespace risk_core {

/**
 * SAX handler for parsing Portfolio JSON using RapidJSON.
 */
class PortfolioHandler {
public:
    PortfolioHandler(Portfolio& portfolio) : portfolio_(portfolio) {}
    
    bool Null() { return true; }
    bool Bool(bool) { return true; }
    bool Int(int) { return true; }
    bool Uint(unsigned) { return true; }
    bool Int64(int64_t) { return true; }
    bool Uint64(uint64_t) { return true; }
    bool Double(double d);
    bool RawNumber(const char* str, size_t length, bool copy);
    bool String(const char* str, size_t length, bool copy);
    bool StartObject();
    bool Key(const char* str, size_t length, bool copy);
    bool EndObject(size_t memberCount);
    bool StartArray();
    bool EndArray(size_t elementCount);
    
    bool HasError() const { return has_error_; }
    const std::string& ErrorMessage() const { return error_message_; }

private:
    Portfolio& portfolio_;
    bool has_error_ = false;
    std::string error_message_;
    
    enum class State {
        Root,
        PortfolioId,
        Assets,
        Asset,
        AssetId,
        AssetCurrency,
        AssetValue
    };
    
    State state_ = State::Root;
    Asset current_asset_;
    std::string current_key_;
};

/**
 * SAX handler for parsing Scenario JSON using RapidJSON.
 */
class ScenarioHandler {
public:
    ScenarioHandler(Scenario& scenario) : scenario_(scenario) {}
    
    bool Null() { return true; }
    bool Bool(bool) { return true; }
    bool Int(int) { return true; }
    bool Uint(unsigned) { return true; }
    bool Int64(int64_t) { return true; }
    bool Uint64(uint64_t) { return true; }
    bool Double(double d);
    bool RawNumber(const char* str, size_t length, bool copy);
    bool String(const char* str, size_t length, bool copy);
    bool StartObject();
    bool Key(const char* str, size_t length, bool copy);
    bool EndObject(size_t memberCount);
    bool StartArray();
    bool EndArray(size_t elementCount);
    
    bool HasError() const { return has_error_; }
    const std::string& ErrorMessage() const { return error_message_; }

private:
    Scenario& scenario_;
    bool has_error_ = false;
    std::string error_message_;
    
    enum class State {
        Root,
        ScenarioId,
        ScenarioName,
        MarketMovementBps,
        VolatilityChangeBps,
        InterestRateChangeBps,
        CurrencyRateChanges,
        CurrencyRateChangeValue
    };
    
    State state_ = State::Root;
    std::string current_key_;
    std::string current_currency_;
};

/**
 * Utility class for parsing JSON files using RapidJSON SAX parser.
 */
class JsonParser {
public:
    /**
     * Parse a portfolio from JSON file.
     * @param filepath Path to JSON file
     * @param portfolio Portfolio object to populate
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParsePortfolio(const std::string& filepath, Portfolio& portfolio);
    
    /**
     * Parse a portfolio from JSON string.
     * @param json JSON string
     * @param portfolio Portfolio object to populate
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParsePortfolioFromString(const std::string& json, Portfolio& portfolio);
    
    /**
     * Parse a scenario from JSON file.
     * @param filepath Path to JSON file
     * @param scenario Scenario object to populate
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParseScenario(const std::string& filepath, Scenario& scenario);
    
    /**
     * Parse a scenario from JSON string.
     * @param json JSON string
     * @param scenario Scenario object to populate
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParseScenarioFromString(const std::string& json, Scenario& scenario);
    
    /**
     * Parse multiple scenarios from JSON file (array or single object).
     * @param filepath Path to JSON file
     * @param scenarios Vector to populate with scenarios
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParseScenarios(const std::string& filepath, std::vector<Scenario>& scenarios);
    
    /**
     * Parse multiple scenarios from JSON string.
     * @param json JSON string
     * @param scenarios Vector to populate with scenarios
     * @return true if parsing succeeded, false otherwise
     */
    static bool ParseScenariosFromString(const std::string& json, std::vector<Scenario>& scenarios);

private:
    static std::string ReadFile(const std::string& filepath);
};

} // namespace risk_core

#endif // RISK_CORE_JSON_PARSER_HPP


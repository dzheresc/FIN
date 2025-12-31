#include "risk_core/json_parser.hpp"
#include <fstream>
#include <sstream>
#include <rapidjson/reader.h>
#include <rapidjson/istreamwrapper.h>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/error/en.h>

namespace risk_core {

// PortfolioHandler implementation
bool PortfolioHandler::Double(double d) {
    if (state_ == State::AssetValue) {
        current_asset_.set_value(d);
        state_ = State::Asset;
    }
    return true;
}

bool PortfolioHandler::RawNumber(const char* str, size_t length, bool copy) {
    double value = std::stod(std::string(str, length));
    return Double(value);
}

bool PortfolioHandler::String(const char* str, size_t length, bool copy) {
    std::string value(str, length);
    
    if (state_ == State::PortfolioId) {
        portfolio_.set_portfolio_id(value);
        state_ = State::Root;
    } else if (state_ == State::AssetId) {
        current_asset_.set_id(value);
        state_ = State::Asset;
    } else if (state_ == State::AssetCurrency) {
        current_asset_.set_currency(value);
        state_ = State::Asset;
    }
    return true;
}

bool PortfolioHandler::StartObject() {
    if (state_ == State::Root) {
        // Root object
    } else if (state_ == State::Assets) {
        state_ = State::Asset;
        current_asset_ = Asset();
    }
    return true;
}

bool PortfolioHandler::Key(const char* str, size_t length, bool copy) {
    std::string key(str, length);
    current_key_ = key;
    
    if (key == "portfolio_id") {
        state_ = State::PortfolioId;
    } else if (key == "assets") {
        state_ = State::Assets;
    } else if (state_ == State::Asset) {
        if (key == "id") {
            state_ = State::AssetId;
        } else if (key == "currency") {
            state_ = State::AssetCurrency;
        } else if (key == "value") {
            state_ = State::AssetValue;
        }
    }
    return true;
}

bool PortfolioHandler::EndObject(size_t memberCount) {
    if (state_ == State::Asset) {
        portfolio_.add_asset(current_asset_);
        state_ = State::Assets;
    } else if (state_ == State::Root || state_ == State::Assets) {
        state_ = State::Root;
    }
    return true;
}

bool PortfolioHandler::StartArray() {
    if (state_ == State::Assets) {
        // Assets array started
    }
    return true;
}

bool PortfolioHandler::EndArray(size_t elementCount) {
    if (state_ == State::Assets) {
        state_ = State::Root;
    }
    return true;
}

// ScenarioHandler implementation
bool ScenarioHandler::Double(double d) {
    if (state_ == State::MarketMovementBps) {
        scenario_.set_market_movement_bps(d);
        state_ = State::Root;
    } else if (state_ == State::VolatilityChangeBps) {
        scenario_.set_volatility_change_bps(d);
        state_ = State::Root;
    } else if (state_ == State::InterestRateChangeBps) {
        scenario_.set_interest_rate_change_bps(d);
        state_ = State::Root;
    } else if (state_ == State::CurrencyRateChangeValue) {
        scenario_.set_currency_rate_change(current_currency_, d);
        state_ = State::CurrencyRateChanges;
    }
    return true;
}

bool ScenarioHandler::RawNumber(const char* str, size_t length, bool copy) {
    double value = std::stod(std::string(str, length));
    return Double(value);
}

bool ScenarioHandler::String(const char* str, size_t length, bool copy) {
    std::string value(str, length);
    
    if (state_ == State::ScenarioId) {
        scenario_.set_scenario_id(value);
        state_ = State::Root;
    } else if (state_ == State::ScenarioName) {
        scenario_.set_scenario_name(value);
        state_ = State::Root;
    }
    return true;
}

bool ScenarioHandler::StartObject() {
    if (state_ == State::Root) {
        // Root object
    } else if (state_ == State::CurrencyRateChanges) {
        // Currency rate changes object
    }
    return true;
}

bool ScenarioHandler::Key(const char* str, size_t length, bool copy) {
    std::string key(str, length);
    current_key_ = key;
    
    if (key == "scenario_id") {
        state_ = State::ScenarioId;
    } else if (key == "scenario_name") {
        state_ = State::ScenarioName;
    } else if (key == "market_movement_bps") {
        state_ = State::MarketMovementBps;
    } else if (key == "volatility_change_bps") {
        state_ = State::VolatilityChangeBps;
    } else if (key == "interest_rate_change_bps") {
        state_ = State::InterestRateChangeBps;
    } else if (key == "currency_rate_changes") {
        state_ = State::CurrencyRateChanges;
    } else if (state_ == State::CurrencyRateChanges) {
        // This is a currency code key
        current_currency_ = key;
        state_ = State::CurrencyRateChangeValue;
    }
    return true;
}

bool ScenarioHandler::EndObject(size_t memberCount) {
    if (state_ == State::CurrencyRateChanges || state_ == State::CurrencyRateChangeValue) {
        state_ = State::Root;
    }
    return true;
}

bool ScenarioHandler::StartArray() {
    return true;
}

bool ScenarioHandler::EndArray(size_t elementCount) {
    return true;
}

// JsonParser implementation
std::string JsonParser::ReadFile(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        return "";
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

bool JsonParser::ParsePortfolio(const std::string& filepath, Portfolio& portfolio) {
    std::string json = ReadFile(filepath);
    if (json.empty()) {
        return false;
    }
    return ParsePortfolioFromString(json, portfolio);
}

bool JsonParser::ParsePortfolioFromString(const std::string& json, Portfolio& portfolio) {
    PortfolioHandler handler(portfolio);
    rapidjson::Reader reader;
    rapidjson::StringStream ss(json.c_str(), json.length());
    
    if (!reader.Parse(ss, handler)) {
        return false;
    }
    
    return !handler.HasError();
}

bool JsonParser::ParseScenario(const std::string& filepath, Scenario& scenario) {
    std::string json = ReadFile(filepath);
    if (json.empty()) {
        return false;
    }
    return ParseScenarioFromString(json, scenario);
}

bool JsonParser::ParseScenarioFromString(const std::string& json, Scenario& scenario) {
    ScenarioHandler handler(scenario);
    rapidjson::Reader reader;
    rapidjson::StringStream ss(json.c_str(), json.length());
    
    if (!reader.Parse(ss, handler)) {
        return false;
    }
    
    return !handler.HasError();
}

bool JsonParser::ParseScenarios(const std::string& filepath, std::vector<Scenario>& scenarios) {
    std::string json = ReadFile(filepath);
    if (json.empty()) {
        return false;
    }
    return ParseScenariosFromString(json, scenarios);
}

bool JsonParser::ParseScenariosFromString(const std::string& json, std::vector<Scenario>& scenarios) {
    // Check if it's an array or single object
    rapidjson::Document doc;
    doc.Parse(json.c_str());
    
    if (doc.HasParseError()) {
        return false;
    }
    
    if (doc.IsArray()) {
        for (const auto& item : doc.GetArray()) {
            rapidjson::StringBuffer buffer;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
            item.Accept(writer);
            
            Scenario scenario;
            if (ParseScenarioFromString(buffer.GetString(), scenario)) {
                scenarios.push_back(scenario);
            }
        }
    } else if (doc.IsObject()) {
        Scenario scenario;
        if (ParseScenarioFromString(json, scenario)) {
            scenarios.push_back(scenario);
        }
    } else {
        return false;
    }
    
    return true;
}

} // namespace risk_core


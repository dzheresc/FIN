#include <gtest/gtest.h>
#include "batch_processor/processor.hpp"
#include "risk_core/json_parser.hpp"
#include "risk_core/validators.hpp"
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

class BatchProcessorTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create test output directory
        test_output_dir_ = fs::temp_directory_path() / "risk_test";
        fs::create_directories(test_output_dir_);
    }
    
    void TearDown() override {
        // Cleanup test files
        if (fs::exists(test_output_dir_)) {
            fs::remove_all(test_output_dir_);
        }
    }
    
    fs::path test_output_dir_;
};

TEST_F(BatchProcessorTest, ProcessPortfolioAndScenarios) {
    std::string portfolio_file = "../../tests/fixtures/sample_portfolio.json";
    std::string scenarios_file = "../../tests/fixtures/sample_scenarios.json";
    std::string output_file = (test_output_dir_ / "results.csv").string();
    
    batch_processor::BatchProcessor processor("USD");
    
    ASSERT_NO_THROW({
        std::string run_id = processor.process(portfolio_file, scenarios_file, output_file);
        EXPECT_FALSE(run_id.empty());
    });
    
    // Verify output file exists
    EXPECT_TRUE(fs::exists(output_file));
    
    // Verify output file has content
    std::ifstream file(output_file);
    ASSERT_TRUE(file.is_open());
    
    std::string line;
    std::getline(file, line); // Read header
    EXPECT_FALSE(line.empty());
    EXPECT_NE(line.find("run_id"), std::string::npos);
}

TEST_F(BatchProcessorTest, InvalidPortfolioFile) {
    batch_processor::BatchProcessor processor;
    
    EXPECT_THROW({
        processor.process("nonexistent.json", "scenarios.json", "output.csv");
    }, std::runtime_error);
}

TEST_F(BatchProcessorTest, DifferentBaseCurrency) {
    std::string portfolio_file = "../../tests/fixtures/sample_portfolio.json";
    std::string scenarios_file = "../../tests/fixtures/sample_scenarios.json";
    std::string output_file = (test_output_dir_ / "results_eur.csv").string();
    
    batch_processor::BatchProcessor processor("EUR");
    
    ASSERT_NO_THROW({
        std::string run_id = processor.process(portfolio_file, scenarios_file, output_file);
        EXPECT_FALSE(run_id.empty());
    });
    
    EXPECT_TRUE(fs::exists(output_file));
}

TEST(JsonParserTest, ParsePortfolio) {
    std::string portfolio_file = "../../tests/fixtures/sample_portfolio.json";
    risk_core::Portfolio portfolio;
    
    EXPECT_TRUE(risk_core::JsonParser::ParsePortfolio(portfolio_file, portfolio));
    EXPECT_FALSE(portfolio.portfolio_id().empty());
    EXPECT_GT(portfolio.assets().size(), 0);
}

TEST(JsonParserTest, ParseScenarios) {
    std::string scenarios_file = "../../tests/fixtures/sample_scenarios.json";
    std::vector<risk_core::Scenario> scenarios;
    
    EXPECT_TRUE(risk_core::JsonParser::ParseScenarios(scenarios_file, scenarios));
    EXPECT_GT(scenarios.size(), 0);
}

TEST(ValidationTest, ValidatePortfolio) {
    risk_core::Portfolio portfolio;
    
    // Empty portfolio should fail
    EXPECT_THROW({
        risk_core::validate_portfolio(portfolio);
    }, risk_core::ValidationError);
    
    // Add valid asset
    risk_core::Asset asset("ASSET001", "USD", 1000.0);
    portfolio.add_asset(asset);
    
    // Should not throw
    EXPECT_NO_THROW({
        risk_core::validate_portfolio(portfolio);
    });
}

TEST(ValidationTest, ValidateAsset) {
    // Valid asset
    risk_core::Asset valid_asset("ASSET001", "USD", 1000.0);
    EXPECT_NO_THROW({
        risk_core::validate_asset(valid_asset);
    });
    
    // Invalid currency
    risk_core::Asset invalid_currency("ASSET002", "XX", 1000.0);
    EXPECT_THROW({
        risk_core::validate_asset(invalid_currency);
    }, risk_core::ValidationError);
    
    // Negative value
    risk_core::Asset negative_value("ASSET003", "USD", -100.0);
    EXPECT_THROW({
        risk_core::validate_asset(negative_value);
    }, risk_core::ValidationError);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}


# Risk Core C++ Implementation

C++ implementation of the risk_core library using RapidJSON with SAX parser for efficient JSON parsing.

## Features

- **Efficient JSON Parsing**: Uses RapidJSON SAX parser for memory-efficient parsing
- **Portfolio Management**: Load and manage multi-currency portfolios
- **Scenario Application**: Apply market scenarios with basis point precision
- **Currency Conversion**: Handle multi-currency portfolios with rate changes
- **Input Validation**: Comprehensive validation of inputs
- **C++17 Standard**: Modern C++ features

## Building

### Prerequisites

- CMake 3.15 or higher
- C++17 compatible compiler (GCC 7+, Clang 5+, MSVC 2017+)
- RapidJSON (automatically downloaded if not found)

### Build Instructions

```bash
mkdir build
cd build
cmake ..
make
```

### Build Options

- `BUILD_TESTS=ON` - Build test suite (default: ON)
- `BUILD_EXAMPLES=ON` - Build example programs (default: ON)

Example:
```bash
cmake -DBUILD_TESTS=OFF ..
```

## Usage

### Basic Example

```cpp
#include "risk_core/json_parser.hpp"
#include "risk_core/portfolio.hpp"
#include "risk_core/scenario.hpp"

using namespace risk_core;

// Load portfolio
Portfolio portfolio;
JsonParser::ParsePortfolio("portfolio.json", portfolio);

// Load scenario
Scenario scenario;
JsonParser::ParseScenario("scenario.json", scenario);

// Apply scenario
ScenarioApplicator applicator(scenario);
auto adjusted_values = applicator.apply_to_portfolio(portfolio, "USD");

// Calculate portfolio total
PortfolioManager manager(portfolio);
double total = manager.total_value("USD");
```

### Running Examples

```bash
cd build
./examples/example_batch
```

## API Overview

### Models

- `Asset` - Represents a single financial asset
- `Portfolio` - Collection of assets
- `Scenario` - Market scenario with risk factors
- `PortfolioResult` - Results of scenario application

### Core Classes

- `JsonParser` - Parse JSON files using RapidJSON SAX
- `PortfolioManager` - Portfolio operations and calculations
- `ScenarioApplicator` - Apply scenarios to portfolios
- `CurrencyConverter` - Currency conversion utilities
- `ValidationError` - Exception for validation failures

### JSON Parsing

The library uses RapidJSON's SAX parser for efficient, streaming JSON parsing:

```cpp
// Parse portfolio
Portfolio portfolio;
JsonParser::ParsePortfolio("portfolio.json", portfolio);

// Parse scenario
Scenario scenario;
JsonParser::ParseScenario("scenario.json", scenario);

// Parse multiple scenarios
std::vector<Scenario> scenarios;
JsonParser::ParseScenarios("scenarios.json", scenarios);
```

## File Structure

```
risk_core_cpp/
├── include/risk_core/     # Header files
│   ├── models.hpp
│   ├── json_parser.hpp
│   ├── portfolio.hpp
│   ├── scenario.hpp
│   ├── currency.hpp
│   ├── calculations.hpp
│   └── validators.hpp
├── src/                   # Implementation files
│   ├── json_parser.cpp
│   ├── portfolio.cpp
│   ├── scenario.cpp
│   ├── currency.cpp
│   ├── calculations.cpp
│   └── validators.cpp
├── examples/              # Example programs
│   └── example_batch.cpp
├── tests/                 # Test suite
├── CMakeLists.txt
└── README.md
```

## Design Decisions

### RapidJSON SAX Parser

The implementation uses RapidJSON's SAX (Simple API for XML) parser instead of DOM parser for:

- **Memory Efficiency**: SAX parser is streaming and doesn't load entire JSON into memory
- **Performance**: Faster parsing for large JSON files
- **Scalability**: Better for processing large portfolios with many assets

### Basis Points Precision

All financial calculations use basis points (1/100th of a percent) for precision:
- 100 bps = 1%
- Calculations use double precision floating point
- For production use, consider using fixed-point or decimal libraries for exact precision

## Integration with Python

This C++ implementation provides the same API as the Python `risk_core` module, making it easy to:

1. Use C++ for performance-critical calculations
2. Maintain Python for rapid development and testing
3. Share the same JSON input/output formats

## License

[Add your license here]


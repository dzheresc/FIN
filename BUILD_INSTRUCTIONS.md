# Build Instructions for C++ Implementation

## RedHat 9 Build

### Prerequisites

```bash
# Install development tools
sudo dnf install -y gcc-c++ cmake make git
```

### Local Build

```bash
# Clone or navigate to project directory
cd /path/to/financial-risk-system

# Create build directory
mkdir build
cd build

# Configure
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(nproc)

# Run tests
ctest --output-on-failure
```

### Docker Build

#### Option 1: Development Build

```bash
docker build -f Dockerfile.rh9 -t financial-risk-system:dev .
docker run -it -v $(pwd):/workspace financial-risk-system:dev
```

#### Option 2: Complete Multi-Stage Build

```bash
docker build -f Dockerfile.rh9.complete -t financial-risk-system:complete .
```

#### Option 3: Using Docker Compose

```bash
docker-compose build
docker-compose up batch-processor
docker-compose up api-service
```

## Running

### Batch Processor

```bash
./build/batch_processor_cpp \
    tests/fixtures/sample_portfolio.json \
    tests/fixtures/sample_scenarios.json \
    output/results.csv \
    --base-currency USD
```

### API Service

```bash
./build/api_service_cpp 5000
```

Test with:
```bash
curl http://localhost:5000/api/v1/health
```

## Testing

```bash
cd build
./tests_cpp/run_tests
```

Or with CTest:
```bash
ctest -V
```

## Troubleshooting

### Missing Dependencies

If RapidJSON or Google Test are not found, CMake will automatically download them via FetchContent.

### Compilation Errors

Ensure you have:
- GCC 9+ (C++17 support)
- CMake 3.15+
- Standard development tools

### Runtime Errors

- Ensure input JSON files exist and are valid
- Check file permissions for output directory
- Verify port availability for API service


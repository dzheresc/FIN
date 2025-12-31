# Financial Risk Evaluation System - C++ Implementation

Complete C++ implementation of the Financial Risk Evaluation System targeting RedHat 9.

## Components

1. **risk_core_cpp** - Core library with RapidJSON SAX parsing
2. **batch_processor_cpp** - Batch processing executable
3. **api_service_cpp** - REST API service (using cpp-httplib)
4. **tests_cpp** - Google Test based test suite

## Building

### Prerequisites

- RedHat 9 (RHEL 9, Rocky Linux 9, or AlmaLinux 9)
- CMake 3.15+
- GCC 9+ (C++17 support)
- Development tools: `gcc-c++`, `cmake`, `make`, `git`

### Local Build

```bash
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Build Options

- `BUILD_TESTS=ON` - Build test suite (default: ON)
- `BUILD_EXAMPLES=ON` - Build examples (default: ON)
- `BUILD_API_SERVICE=ON` - Build API service (default: ON)

## Docker Build (RedHat 9)

### Single Stage Build

```bash
docker build -f Dockerfile.rh9 -t financial-risk-system:builder .
```

### Multi-Stage Complete Build

```bash
docker build -f Dockerfile.rh9.complete -t financial-risk-system:complete .
```

### Using Docker Compose

```bash
docker-compose build
docker-compose up
```

## Usage

### Batch Processor

```bash
./build/batch_processor_cpp \
    portfolio.json \
    scenarios.json \
    output.csv \
    --base-currency USD
```

### API Service

```bash
./build/api_service_cpp 5000
```

The API will be available at `http://localhost:5000`

### API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/evaluate` - Evaluate portfolio against scenario
- `POST /api/v1/batch/evaluate` - Batch evaluation
- `GET /api/v1/runs/{run_id}` - Get evaluation run
- `GET /api/v1/runs` - List runs

## Testing

### Run Tests

```bash
cd build
ctest --output-on-failure
```

Or run the test executable directly:

```bash
./build/tests_cpp/run_tests
```

### Test Coverage

Tests cover:
- JSON parsing (RapidJSON SAX)
- Portfolio operations
- Scenario application
- Currency conversion
- Input validation
- Batch processing workflow

## Dependencies

### Automatic Fetching

The build system automatically fetches:
- **RapidJSON** - JSON parsing (SAX parser)
- **Google Test** - Testing framework
- **cpp-httplib** - HTTP server library

### System Dependencies

- Standard C++ library (libstdc++)
- No external runtime dependencies required

## RedHat 9 Specific Notes

### Base Image

Uses `registry.access.redhat.com/ubi9/ubi:latest` (Universal Base Image)

### Package Manager

Uses `dnf` (Dandified YUM) for package management

### Compatibility

Tested on:
- RedHat Enterprise Linux 9
- Rocky Linux 9
- AlmaLinux 9

## Performance

### Advantages of C++ Implementation

- **Memory Efficiency**: SAX parsing doesn't load entire JSON into memory
- **Performance**: Native compilation for optimal speed
- **Scalability**: Handles large portfolios efficiently
- **Resource Usage**: Lower memory footprint than interpreted languages

## Integration

The C++ implementation uses the same JSON input/output formats as the Python version, enabling:

- Shared test fixtures
- Interoperable data formats
- Easy migration between implementations
- Performance-critical paths in C++, rapid development in Python

## Troubleshooting

### Build Issues

1. **Missing CMake**: Install with `dnf install cmake`
2. **C++17 not supported**: Ensure GCC 9+ is installed
3. **RapidJSON not found**: Will be automatically downloaded

### Runtime Issues

1. **Library not found**: Ensure `libstdc++` is installed
2. **Port already in use**: Change API service port
3. **File permissions**: Check input/output file permissions

## License

[Add your license here]


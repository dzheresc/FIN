cmake_minimum_required(VERSION 3.15)
project(risk_core_cpp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Options
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Find or include RapidJSON
# Option 1: If RapidJSON is installed system-wide
find_path(RAPIDJSON_INCLUDE_DIR rapidjson/rapidjson.h
    PATHS
    /usr/include
    /usr/local/include
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/rapidjson/include
)

if(NOT RAPIDJSON_INCLUDE_DIR)
    # Option 2: Download RapidJSON if not found
    include(FetchContent)
    FetchContent_Declare(
        rapidjson
        GIT_REPOSITORY https://github.com/Tencent/rapidjson.git
        GIT_TAG v1.1.0
    )
    FetchContent_MakeAvailable(rapidjson)
    set(RAPIDJSON_INCLUDE_DIR ${rapidjson_SOURCE_DIR}/include)
endif()

include_directories(${RAPIDJSON_INCLUDE_DIR})

# Source files
set(RISK_CORE_SOURCES
    src/json_parser.cpp
    src/portfolio.cpp
    src/scenario.cpp
    src/currency.cpp
    src/calculations.cpp
    src/validators.cpp
)

# Header files
set(RISK_CORE_HEADERS
    include/risk_core/models.hpp
    include/risk_core/json_parser.hpp
    include/risk_core/portfolio.hpp
    include/risk_core/scenario.hpp
    include/risk_core/currency.hpp
    include/risk_core/calculations.hpp
    include/risk_core/validators.hpp
)

# Create library
add_library(risk_core_cpp STATIC
    ${RISK_CORE_SOURCES}
    ${RISK_CORE_HEADERS}
)

target_include_directories(risk_core_cpp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Build examples if enabled
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Build tests if enabled
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Installation
install(TARGETS risk_core_cpp
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(DIRECTORY include/risk_core
    DESTINATION include
    FILES_MATCHING PATTERN "*.hpp"
)


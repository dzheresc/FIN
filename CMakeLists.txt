cmake_minimum_required(VERSION 3.15)
project(FinancialRiskSystem VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Options
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)
option(BUILD_API_SERVICE "Build API service" ON)

# Include subdirectories
add_subdirectory(risk_core_cpp)
add_subdirectory(batch_processor_cpp)

if(BUILD_API_SERVICE)
    add_subdirectory(api_service_cpp)
endif()

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests_cpp)
endif()

if(BUILD_EXAMPLES)
    add_subdirectory(risk_core_cpp/examples)
endif()


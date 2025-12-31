cmake_minimum_required(VERSION 3.15)

# Find Google Test
find_package(GTest QUIET)

if(NOT GTest_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.14.0
    )
    FetchContent_MakeAvailable(googletest)
endif()

# Test source files
set(TEST_SOURCES
    test_batch_processor.cpp
)

# Create test executable
add_executable(run_tests ${TEST_SOURCES})

target_include_directories(run_tests PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/..
)

target_link_libraries(run_tests
    risk_core_cpp
    batch_processor_cpp
    GTest::gtest
    GTest::gtest_main
)

# Add test
add_test(NAME BatchProcessorTests COMMAND run_tests)


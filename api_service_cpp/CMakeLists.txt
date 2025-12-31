cmake_minimum_required(VERSION 3.15)

# Find or download cpp-httplib
find_path(HTTPLIB_INCLUDE_DIR httplib.h
    PATHS
    /usr/include
    /usr/local/include
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/cpp-httplib
)

if(NOT HTTPLIB_INCLUDE_DIR)
    include(FetchContent)
    FetchContent_Declare(
        httplib
        GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git
        GIT_TAG v0.14.3
    )
    FetchContent_MakeAvailable(httplib)
    set(HTTPLIB_INCLUDE_DIR ${httplib_SOURCE_DIR})
endif()

include_directories(${HTTPLIB_INCLUDE_DIR})

# Source files
set(API_SERVICE_SOURCES
    src/server.cpp
    src/main.cpp
)

# Header files
set(API_SERVICE_HEADERS
    include/api_service/server.hpp
)

# Create executable
add_executable(api_service_cpp
    ${API_SERVICE_SOURCES}
    ${API_SERVICE_HEADERS}
)

target_include_directories(api_service_cpp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries(api_service_cpp
    risk_core_cpp
    batch_processor_cpp
)


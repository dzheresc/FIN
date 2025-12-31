cmake_minimum_required(VERSION 3.15)

# Source files
set(BATCH_PROCESSOR_SOURCES
    src/processor.cpp
    src/csv_writer.cpp
    src/main.cpp
)

# Header files
set(BATCH_PROCESSOR_HEADERS
    include/batch_processor/processor.hpp
    include/batch_processor/csv_writer.hpp
)

# Create executable
add_executable(batch_processor_cpp
    ${BATCH_PROCESSOR_SOURCES}
    ${BATCH_PROCESSOR_HEADERS}
)

target_include_directories(batch_processor_cpp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries(batch_processor_cpp
    risk_core_cpp
)


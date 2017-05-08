cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_COMPILER /Users/jon/DEV/llvm-github/clang-build/bin/clang++)
set(CMAKE_CXX_STANDARD 14)

add_executable(fuzz_divider fuzz_divider.cpp)
target_compile_options(fuzz_divider PUBLIC -fsanitize=fuzzer,undefined,address)
set_property(TARGET fuzz_divider APPEND PROPERTY LINK_FLAGS -fsanitize=fuzzer,undefined,address)

enable_testing()

add_test(
  NAME fuzz_divider
  COMMAND ./fuzz_divider
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

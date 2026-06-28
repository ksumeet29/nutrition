cmake_minimum_required(VERSION 4.1)
project(Nutrition)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(nutrition
    src/main.cpp
    src/tdee.cpp
    src/macros.cpp
    src/utils.cpp
)

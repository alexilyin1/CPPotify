cmake_minimum_required(VERSION 3.16)
project("pybind11module_CPPotify")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_PREFIX_PATH /usr/include/)

set(APP_SOURCE "${PROJECT_SOURCE_DIR}/source/app")
set(MODULE_SOURCE "${PROJECT_SOURCE_DIR}/source/module")
set(EXTERNALS "${PROJECT_SOURCE_DIR}/externals")

add_subdirectory(${EXTERNALS}/pybind11-2.6.1)

pybind11_add_module (
    pybind11module 
    ${MODULE_SOURCE}/CPPotify.cpp
    ${MODULE_SOURCE}/CPPotify.h
    ${MODULE_SOURCE}/authControl.cpp
    ${MODULE_SOURCE}/authControl.h
)

target_link_libraries(
    pybind11module
    PRIVATE curl
    PRIVATE nlohmann_json::nlohmann_json
)

target_include_directories (
    pybind11module 
    PRIVATE ${MODULE_SOURCE}
)

add_executable (
    pybind11app
    ${APP_SOURCE}/app.cpp
    ${MODULE_SOURCE}/CPPotify.cpp
    ${MODULE_SOURCE}/CPPotify.h
    ${MODULE_SOURCE}/authControl.cpp
    ${MODULE_SOURCE}/authControl.h
)

target_include_directories (
    pybind11app 
    PRIVATE ${APP_SOURCE}
    PRIVATE ${MODULE_SOURCE}
)

find_package(nlohmann_json 3.2.0 REQUIRED)

target_link_libraries(
    pybind11app
    PRIVATE pybind11::embed
    curl
    nlohmann_json::nlohmann_json
)
cmake_minimum_required(VERSION 3.12)
# Project
#get_filename_component(PROJECT_DIR "${CMAKE_CURRENT_SOURCE_DIR}" ABSOLUTE)
#set(DEPENDENCIES_DIR ${PROJECT_DIR}/dependencies)
set(PROJECT_NAME natlink)
set(CMAKE_CXX_STANDARD 14)


# make binary python callable
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
set(BUILD_SHARED_LIBS  ON)

project(${PROJECT_NAME})

# Source Files
set(SRC_FILES
        COM/appsupp.cpp
        DictationObject.cpp
        DragonCode.cpp
        Exceptions.cpp
        GrammarObject.cpp
        natlink.cpp
        pythwrap.cpp
        ResultObject.cpp
        MessageWindow.cpp
        StdAfx.cpp
        natlink.rc
        )
source_group("Sources" FILES ${SRC_FILES})

# Header Files
set(HEADERS_FILES
        COM/appsupp.h
        COM/comsupp.h
        DictationObject.h
        DragonCode.h
        COM/dspeech.h
        Exceptions.h
        GrammarObject.h
        ResultObject.h
        Resource.h
        MessageWindow.h
        COM/speech.h
        StdAfx.h
        )
source_group("Headers" FILES ${HEADERS_FILES})

# TODO This should not be hard coded...
include_directories("C:\\Python37_32bit\\include")
include_directories("extern")
link_directories("C:\\Python37_32bit\\libs")

add_compile_definitions(DRAGON_VERSION=15)
# Asserts that Py_ssize_t is used in argument parsing,
# see note at top of https://docs.python.org/3/c-api/arg.html
add_compile_definitions(PY_SSIZE_T_CLEAN)

# Ensures a Stable Application Binary Interface forpython 3.2+
#add_compile_definitions(Py_LIMITED_API)

# ensures that both the stdlib and vc runtime are statically linked into
# the DLL -> fewer dependencies for the user
foreach(flag_var
        CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE
        CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO)

    message(${flag_var})
    if(${flag_var} MATCHES "/MD")
        string(REGEX REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
    endif(${flag_var} MATCHES "/MD")
endforeach(flag_var)

# Add library to build.
add_library(${PROJECT_NAME} SHARED
        ${SRC_FILES} #${HEADERS_FILES}
        )
set_target_properties(
        ${PROJECT_NAME}
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "natlink"
        LINKER_LANGUAGE C
)
SET_TARGET_PROPERTIES(${PROJECT_NAME}   PROPERTIES SUFFIX .pyd)

MACRO(SET_IF_EMPTY _variable)
  IF("${${_variable}}" STREQUAL "")
    SET(${_variable} ${ARGN})
  ENDIF()
ENDMACRO()

MACRO(VERBOSE_INCLUDE _file)
  MESSAGE(STATUS "")
  MESSAGE(STATUS "Include ${_file}")
  INCLUDE(${_file})
ENDMACRO()

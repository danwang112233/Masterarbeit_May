###############################################################################
##
## Project name, version, Custom CMake functions
##
###############################################################################

CMAKE_MINIMUM_REQUIRED( VERSION 2.8)

PROJECT( LAMMPS )

SET( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/cmake )
MESSAGE( STATUS "Include MACROS.cmake" )
#INCLUDE( macros )

###############################################################################
##
## Definition of build options
##
###############################################################################

OPTION( LAMMPS_BUILD_EXECUTABLE        "Build lammps executable"        ON  )
OPTION( LAMMPS_BUILD_STATIC_LIB        "Build lammps static library"    ON  )
OPTION( LAMMPS_BUILD_SHARED_LIB        "Build lammps shared library"    ON  )

OPTION( LAMMPS_ENABLE_KSPACE           "Use the KSPACE package"         ON  )

OPTION( LAMMPS_WITH_MPI                "Build with MPI"                 OFF )
OPTION( LAMMPS_WITH_JPEG               "Build with JPEG"                OFF )
OPTION( LAMMPS_WITH_PYTHON_EXTENSION   "Build with python interface"    ON  )
#OPTION( LAMMPS_WITH_FFTW               "Build with FFTW"                OFF  )


#-------------------------------------------------DEFAULT BUILD TYPE
IF ( NOT CMAKE_BUILD_TYPE )
    SET ( CMAKE_BUILD_TYPE Release CACHE STRING "Build Types: 
          Debug Release DebugOptimized RelWithDebInfo MinSizeRel."  FORCE )
ENDIF()
SET_PROPERTY( CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS 
          Debug Release DebugOptimized RelWithDebInfo MinSizeRel )

#-------------------------------------------------GNU COMPILER FLAGS SECTION
if(CMAKE_CXX_COMPILER_ID MATCHES GNU)
    set(CMAKE_CXX_FLAGS         "${CMAKE_CXX_FLAGS} -Wall")
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g3")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()


#-------------------------------------------------FFTW
#IF( LAMMPS_ENABLE_KSPACE )
#   EXECUTE_PROCESS( WORKING_DIRECTORY /src COMMAND make yes-KSPACE ERROR_QUIET OUTPUT_QUIET)
#   IF( LAMMPS_WITH_FFTW )
#      FIND_PACKAGE( FFTW REQUIRED )
#      IF( FFTW_FOUND)
#		   ADD_DEFINITIONS(-DLAMMPS_BUILD_WITH_FFTW)
#		   LIST ( APPEND SERVICE_LIBS ${FFTW_LIBRARIES} )
#		   INCLUDE_DIRECTORIES( ${FFTW_INCLUDES} )
#		ENDIF( FFTW_FOUND )
#   ELSE( LAMMPS_WITH_FFTW )	
#		SET(FFT_FLAG FFT_NONE CACHE STRING "FFT compiler flag. See src/fft3d.h for details/options")
#	ENDIF( LAMMPS_WITH_FFTW )
#ELSE( LAMMPS_ENABLE_KSPACE )
#	EXECUTE_PROCESS(WORKING_DIRECTORY ${LAMMPS_SOURCE_DIR}/src COMMAND make no-KSPACE ERROR_QUIET OUTPUT_QUIET)
#ENDIF(LAMMPS_ENABLE_KSPACE )

#-------------------------------------------------MPI SECTION
IF( LAMMPS_WITH_MPI )
	FIND_PACKAGE( MPI REQUIRED )
	IF( MPI_FOUND )
	   LIST( APPEND SERVICE_LIBS ${MPI_LIBRARIES} )
		INCLUDE_DIRECTORIES( ${MPI_INCLUDE_PATH} )
		ADD_DEFINITIONS( -DLAMMPS_BUILD_WITH_MPI )
	ELSE( MPI_FOUND )
		MESSAGE(FATA_ERROR "Could not find any MPI installation, check $PATH.")
	ENDIF( MPI_FOUND )
ELSE( LAMMPS_WITH_MPI )
# TODO FIX THIS
    EXECUTE_PROCESS( WORKING_DIRECTORY ${LAMMPS_SOURCE_DIR}/src COMMAND make yes-STUBS ERROR_QUIET OUTPUT_QUIET )
ENDIF( LAMMPS_WITH_MPI )

#Set up source files:
INCLUDE_DIRECTORIES(src)
AUX_SOURCE_DIRECTORY(src LAMMPS_SRC)

FIND_PACKAGE( PythonLibs REQUIRED )
#INCLUDE_DIRECTORIES( ${MPI_INCLUDE_PATH} )
LIST( APPEND SERVICE_LIBS ${PYTHON_LIBRARIES} )
INCLUDE_DIRECTORIES( ${PYTHON_INCLUDE_DIRS} )

IF ( LAMMPS_WITH_PYTHON_EXTENSION AND LAMMPS_BUILD_EXECUTABLE )
    MESSAGE( WARNING "--Cannot create executable when extending python." )
    MESSAGE( STATUS  "Setting LAMMPS_BUILD_EXECUTABLE OFF" )
    MESSAGE( STATUS  "Setting LAMMPS_BUILD_SHARED_LIB ON" )
    SET( LAMMPS_BUILD_EXECUTABLE OFF CACHE BOOL "Build lammps executable" FORCE )
    SET( LAMMPS_BUILD_SHARED_LIB ON CACHE BOOL "Build lammps shared library" FORCE )
ENDIF( LAMMPS_WITH_PYTHON_EXTENSION AND LAMMPS_BUILD_EXECUTABLE )


###############################################################################
##
## Installation Directory, Library and Executable Name
##
###############################################################################
SET ( CMAKE_INSTALL_PREFIX /usr/local/lammps CACHE STRING 
                           "The default installation directory."   )
IF( LAMMPS_BUILD_SHARED_LIB )
    SET(LAMMPS_LIBRARY_NAME "lammps" CACHE STRING "Name of LAMMPS library.  Note: automatically prepends lib and appends .so")
    ADD_LIBRARY( ${LAMMPS_LIBRARY_NAME} SHARED ${LAMMPS_SRC} ${MPI_LIBRARIES} ${PYTHON_LIBRARIES} )
    TARGET_LINK_LIBRARIES ( ${LAMMPS_LIBRARY_NAME} ${MPI_LIBRARIES} ${PYTHON_LIBRARIES} )
    INSTALL( TARGETS ${LAMMPS_LIBRARY_NAME}
			 RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
		 	 LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
             ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib )
ENDIF( LAMMPS_BUILD_SHARED_LIB )

IF( LAMMPS_BUILD_EXECUTABLE )
    SET(LAMMPS_EXECUTABLE_NAME "lmp" CACHE STRING "Name of LAMMPS executable")
    ADD_EXECUTABLE( ${LAMMPS_EXECUTABLE_NAME} ${LAMMPS_SRC} )
    TARGET_LINK_LIBRARIES ( ${LAMMPS_EXECUTABLE_NAME} ${MPI_LIBRARIES} ${PYTHON_LIBRARIES} )
    INSTALL( TARGETS ${LAMMPS_EXECUTABLE_NAME}
		     RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
		     LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
             ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib )
ENDIF( LAMMPS_BUILD_EXECUTABLE )


# - Try to find FFTW
# Find the native FFTW includes and library
#
#  FFTW_DIR         - where fftw is installed
#  FFTW_INCLUDES    - where to find fftw3.h
#  FFTW_LIBRARIES   - List of libraries when using FFTW.
#  FFTW_FOUND       - True if FFTW found.

SET( FFTW_DIR "" CACHE PATH "An optional hint to a BOOST installation" )
SET_IF_EMPTY(FFTW_DIR "$ENV{FFTW_DIR}")

IF( FFTW_INCLUDES )
  # Already in cache, be silent
  SET( FFTW_FIND_QUIETLY TRUE )
ENDIF( FFTW_INCLUDES )

FIND_PATH( FFTW_INCLUDES 
           NAMES fftw3.h 
           PATH  ${FFTW_DIR} )

FIND_LIBRARY( FFTW_LIBRARIES 
              NAMES fftw3
              PATH  ${FFTW_DIR} )

# handle the QUIETLY and REQUIRED arguments and set FFTW_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE( FindPackageHandleStandardArgs )
FIND_PACKAGE_HANDLE_STANDARD_ARGS( FFTW DEFAULT_MSG FFTW_LIBRARIES FFTW_INCLUDES )

MARK_AS_ADVANCED( FFTW_LIBRARIES FFTW_INCLUDES )

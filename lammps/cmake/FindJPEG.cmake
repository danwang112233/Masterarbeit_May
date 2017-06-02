# - Try to find JPEG
# Find the native JPEG includes and library
#
#  JPEG_DIR         - where fftw is installed
#  JPEG_INCLUDES    - where to find fftw3.h
#  JPEG_LIBRARIES   - List of libraries when using JPEG.
#  JPEG_FOUND       - True if JPEG found.

SET( JPEG_DIR "" CACHE PATH "An optional hint to a BOOST installation" )
SET_IF_EMPTY(JPEG_DIR "$ENV{JPEG_DIR}")

IF( JPEG_INCLUDES )
  # Already in cache, be silent
  SET( JPEG_FIND_QUIETLY TRUE )
ENDIF( JPEG_INCLUDES )

FIND_PATH( JPEG_INCLUDES 
           NAMES jconfig.h jerror.h jmorecfg.h jpeglib.h
           PATH  ${JPEG_DIR} )

FIND_LIBRARY( JPEG_LIBRARIES 
              NAMES jpeg
              PATH  ${JPEG_DIR} )

# handle the QUIETLY and REQUIRED arguments and set JPEG_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE( FindPackageHandleStandardArgs )
FIND_PACKAGE_HANDLE_STANDARD_ARGS( JPEG DEFAULT_MSG JPEG_LIBRARIES JPEG_INCLUDES )

MARK_AS_ADVANCED( JPEG_LIBRARIES JPEG_INCLUDES )

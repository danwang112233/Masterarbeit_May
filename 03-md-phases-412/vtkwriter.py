import errno
import os
import numpy as np
import sys

"""
    Create a (vtk) directory if it is not present in the current directory.
"""
def vtkmkdir( foldername ):
    try:
        os.makedirs( foldername )
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

"""
    Write VTK files inside vtk folder.
    Naming convention for the file:
    180degdm_timestep.vtk
    example: 180degdm_500.vtk
    Naming convention for the folder:
    nm_n_n_efield_summationmethod
    example: 60_6_6_e0.0075_wolf
"""
def write_single_vtk( simbox, step, A, B, keystring):
    e  = simbox['e']
    nx  = simbox['nx']
    ny  = simbox['ny']
    nz  = simbox['nz']
    up  = simbox['up']
    nxm = simbox['nx']*simbox['m']
    run= simbox['run']

    HEADER =    "# vtk DataFile Version 4.0      \n"               + \
                "Domain Wall Movement VTK output \n"               + \
                "ASCII                           \n"               + \
                "DATASET STRUCTURED_GRID         \n"               + \
                "DIMENSIONS %d %d %d             \n" %( nxm, ny, nz)  + \
                "POINTS %d double                \n" %( nxm*ny*nz )

    VEC    = "\nPOINT_DATA %d \nVECTORS polarization double \n" %( nxm*ny*nz )
    vtkfolder    = "vtk/"
    vtksubfolder = "%d_%d_%d_up%d_e%.6f_wolf_%s/" %( nxm, ny, nz, up, e, run)
    vtkfinalpath      = vtkfolder + vtksubfolder
    vtkmkdir( vtkfolder )
    vtkmkdir( vtkfinalpath )
    filename = vtkfinalpath + keystring + "%g" %(step) + ".vtk"
    with file( filename, 'w' ) as fh:
        fh.write( HEADER )
        np.savetxt( fh, A, fmt='%.6e', delimiter='\t')
        fh.write( VEC)
        np.savetxt( fh, B, fmt='%.6e', delimiter='\t')

def write_single_narray( simbox, step, A, keystring ):
    e   = simbox['e']    
    nx  = simbox['nx']
    ny  = simbox['ny']
    nz  = simbox['nz']
    up  = simbox['up']
    nxm = simbox['nx']*simbox['m']
    run = simbox['run']
    h   = simbox['header']
    vtkfolder    = "vtk/"
    vtksubfolder = "%d_%d_%d_up%d_e%.6f_wolf_%s/" %( nxm, ny, nz, up, e, run)
    vtkfinalpath      = vtkfolder + vtksubfolder
    vtkmkdir( vtkfolder )
    vtkmkdir( vtkfinalpath )
    filename = vtkfinalpath + keystring + ".dat"
    with file( filename, 'a' ) as fh:
        np.savetxt( fh, A, fmt='%.6e', delimiter='\t',header=h)

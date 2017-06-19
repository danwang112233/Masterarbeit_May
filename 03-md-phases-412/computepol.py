"""
    Python function takes a file, containng atomic displacement, as input and
    calculates polarization.
    
    180deg domain wall. Wall normal direction - x.
    
    Titanium ions at the corners
    
    Created:  May 2016
    Modified: August 2016
"""
import os, sys
INC_PATH = "../commons/"
sys.path.append(os.path.abspath(INC_PATH))

from aux.volume import volume
from dump import dump
from numpy import linalg as la
from vtkwriter import vtkmkdir, write_single_vtk, write_single_narray
import itertools
import numpy as np

def last_timestep ( filename ):
    d = dump( filename )
    d.tselect.all()          # Select all timesteps
    tlist = d.time()         # Gather a list of all timesteps
    tlast = int( tlist[-1] ) # Store the last timestep in tlast
    return int(tlast)

def pol ( filename, simbox, step ):
    a    = simbox['a']
    e    = simbox['e']
    nx   = simbox['nx']
    ny   = simbox['ny']
    nz   = simbox['nz']
    m    = simbox['m']
    up   = simbox['up']
    cbya = simbox['cbya']

    #tlast = last_timestep( filename )
    d = dump( filename )
    d.tselect.one( step )   # Select the last timestep
    d.aselect.all( step )   # Select all the atomic displacements of tlast
    
    # Core Shell charges taken from [Vielma et al 2013]
    zBaCore  =  4.859
    zBaShell = -2.948
    zTiCore  =  4.555
    zTiShell = -1.615    
    zO1Core  =  1.058
    zO1Shell = -2.675
    zO2Core  =  1.058
    zO2Shell = -2.675
    zO3Core  =  1.058
    zO3Shell = -2.675

    # Read atomic displacements of Ba, Ti, O1, O2, and O3 as a numpy array
    natoms = 10*m*nx*ny*nz
    p = np.zeros( (1,3), dtype=np.float )
    P = np.array([0., 0., 0.])
    lp = np.array([0., 0., 0.])
    rp = np.array([0., 0., 0.])
    
    # Volume of a unit cell
    V = volume( "T", a, None, cbya*a, None, None, None)
    VOL = V * m *nx*ny*nz
    
    # upVOL is the volume with upward polarization
    upVOL = VOL * up / (nx*m)
    dnVOL = VOL - upVOL
    
    if filename =="displdump":
        srstr = "c_dr"
    else:
        srstr = "f_AVE_ATOM"
        
    POL3   = np.empty((0,3), float)
    points = np.empty((0,3), float)
    LP     = np.empty((0,5), float)
    RP     = np.empty((0,5), float)
    
    for i in range(0, nx*m, 1):
        for j in range(0, ny, 1):
            for k in range(0, nz, 1):
                na = 10*(ny*nz*i+nz*j+k)
                TiCore  = d.atom(na+ 1, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                TiShell = d.atom(na+ 2, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                BaCore  = d.atom(na+ 3, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                BaShell = d.atom(na+ 4, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O1Core  = d.atom(na+ 5, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O1Shell = d.atom(na+ 6, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O2Core  = d.atom(na+ 7, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O2Shell = d.atom(na+ 8, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O3Core  = d.atom(na+ 9, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                O3Shell = d.atom(na+10, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
                
                drBaCore  = np.asarray( list( itertools.chain.from_iterable (BaCore ) ))
                drBaShell = np.asarray( list( itertools.chain.from_iterable (BaShell) ))
                drTiCore  = np.asarray( list( itertools.chain.from_iterable (TiCore ) ))
                drTiShell = np.asarray( list( itertools.chain.from_iterable (TiShell) ))
                drO1Core  = np.asarray( list( itertools.chain.from_iterable (O1Core ) ))
                drO1Shell = np.asarray( list( itertools.chain.from_iterable (O1Shell) ))
                drO2Core  = np.asarray( list( itertools.chain.from_iterable (O2Core ) ))
                drO2Shell = np.asarray( list( itertools.chain.from_iterable (O2Shell) ))
                drO3Core  = np.asarray( list( itertools.chain.from_iterable (O3Core ) ))
                drO3Shell = np.asarray( list( itertools.chain.from_iterable (O3Shell) ))

                temp = zBaCore * drBaCore + zBaShell * drBaShell + \
                       zTiCore * drTiCore + zTiShell * drTiShell + \
                       zO1Core * drO1Core + zO1Shell * drO1Shell + \
                       zO2Core * drO2Core + zO2Shell * drO2Shell + \
                       zO3Core * drO3Core + zO3Shell * drO3Shell 
                      
                temp = 1.60217662 * temp * 10.0
                P += temp/ VOL
                
                domain_boundary = 10*up*ny*nz
                if na < domain_boundary:
                    lp += temp/ upVOL
                else:
                    rp += temp/ dnVOL    
                points = np.append( points, np.asarray( [[i, j, k]] ), axis=0 )
                POL3 = np.append( POL3, np.asarray([temp.tolist()] ), axis=0 )
    
    if P[2] < 0.:
        S = -1.
    else:
        S = 1.  
    if lp[2] < 0.:
        LS = -1.
    else:
        LS = 1.  
    if rp[2] < 0.:
        RS = -1.
    else:
        RS = 1.  
        
    LP = np.append( LP, np.asarray([ [step]+lp.tolist()+[LS*la.norm(lp)] ]), axis=0 )
    RP = np.append( RP, np.asarray([ [step]+rp.tolist()+[RS*la.norm(rp)] ]), axis=0 )
    
    print "LP is \n", lp, "\n", "RP is\n", rp
    write_single_vtk(simbox, step, points, POL3, "180degdm_" )
    write_single_narray( simbox, step, LP, "LP" )
    write_single_narray( simbox, step, RP, "RP" )

    with file("LP.dat", 'a') as f:
        np.savetxt(f, LP, delimiter='\t', fmt='%.6e')
    with file("RP.dat", 'a') as f:
        np.savetxt(f, RP, delimiter='\t', fmt='%.6e')

#    with file("polpart.dat", "w") as f:
#        np.savetxt(f, [lp, rp, delimiter='\t' )

    print "The absolute polarization: ", (np.append( P, [ S*la.norm(P)] )).tolist()
    return (np.append( P, [ S*la.norm(P)] )).tolist()

def find_temp( step, filename):
    d = {}
    try:
        with open(filename) as f:
            for line in f:
                l = line.strip()
                if not l.startswith("#"):
                    (key, val) = line.split()
                    d[int(key)] = val
        if step in d:
            return d[step]
        else:
            print "Timestep not found in the file %s" %filename
    except IOError:
        print "The file %s cannot be accessed or not found"  %filename


"""
    Python function takes a file, containng atomic displacement, as input and
    calculates polarization.
    
    Barium at the corners, Titanium at the center and Oxygen at the facecenters.
    
    Created:  May 2016
    Modified: Jul 2016
    
    Vishal Boddu
"""
import os, sys

INC_PATH = "../commons/"
sys.path.append(os.path.abspath(INC_PATH))

from aux.volume import volume
from dump import dump
from numpy import linalg as la
import itertools
import numpy as np

def last_timestep ( filename ):
    d = dump( filename )
    d.tselect.all()          # Select all timesteps
    tlist = d.time()         # Gather a list of all timesteps
    tlast = int( tlist[-1] ) # Store the last timestep in tlast
    return int(tlast)
        
def pol ( filename, a, alpha, nx, ny, nz ):
    a = a
    alpha = alpha
    tlast = last_timestep( filename )
    d = dump( filename )
    d.tselect.one( tlast )   # Select the last timestep
    d.aselect.all( tlast )   # Select all the atomic displacements of tlast
    
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
    natoms = 10 *(nx * ny *nz)
    p = np.zeros( (1,3), dtype=np.float )
    P = np.empty( (0,3), float )
    V = volume( "R", a, None, None, alpha, None, None )

    if filename =="displdump":
        srstr = "c_dr"
    else:
        srstr = "f_AVE_ATOM"
    for i in range(0, natoms, 10):
        BaCore  = d.atom( i+ 1, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        BaShell = d.atom( i+ 2, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        TiCore  = d.atom( i+ 3, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        TiShell = d.atom( i+ 4, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O1Core  = d.atom( i+ 5, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O1Shell = d.atom( i+ 6, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O2Core  = d.atom( i+ 7, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O2Shell = d.atom( i+ 8, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O3Core  = d.atom( i+ 9, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)
        O3Shell = d.atom( i+10, "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr)

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
        temp = 1.60217662 * temp * 10.0 / ( V * nx * ny * nz )
        p += temp 
        
    if p[0][0] < 0. and p[0][1] < 0. and p[0][2] < 0.:
        f = -1.
    else:
        f = 1.  
    print "The absolute polarization: ", (np.append( p, [ f*la.norm(p)] )).tolist()
    return (np.append( p, [ f*la.norm(p)] )).tolist()

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

def find_lat( step, filename):
    d = {}
    try:
        with open(filename) as f:
            for line in f:
                l = line.strip()
                if not l.startswith("#"):
                    items = line.split()
                    key, val = items[0], items[1:]
                    d[int(key)] = val
        if step in d:
            return d[step]
        else:
            print "Timestep not found in the file %s" %filename
    except IOError:
        print "The file %s cannot be accessed or not found"  %filename
        
""" Old Code
    # Born effective charges: Using (dynamic) shell model charges 
    # [Tinte et al 1999], instead of first principle [Zhong et al 1994]
    zBa =  2.172
    zTi =  3.072
    zO1 = -1.748
    zO2 = -1.748
    # Born effect charge tensor
    ZBa = np.array ( [ [zBa, 0.0, 0.0], [ 0.0, zBa, 0.0 ], [ 0.0, 0.0, zBa] ] )
    ZTi = np.array ( [ [zTi, 0.0, 0.0], [ 0.0, zTi, 0.0 ], [ 0.0, 0.0, zTi] ] )
    ZO1 = np.array ( [ [zO1, 0.0, 0.0], [ 0.0, zO2, 0.0 ], [ 0.0, 0.0, zO2] ] )
    ZO2 = np.array ( [ [zO2, 0.0, 0.0], [ 0.0, zO1, 0.0 ], [ 0.0, 0.0, zO2] ] )
    ZO3 = np.array ( [ [zO2, 0.0, 0.0], [ 0.0, zO2, 0.0 ], [ 0.0, 0.0, zO1] ] )
    # Read atomic displacements of Ba, Ti, O1, O2, and O3 as a numpy array
    natoms = 10 *(n**3)
    P = np.array([0., 0., 0.])
    if filename =="displdump":
        srstr = "c_dr"
    else:
        srstr = "f_AVE_ATOM"
    for a in range(0, natoms, 10):
        drBa = np.asarray( list( itertools.chain.from_iterable( d.atom(a+1,\
                       "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr) ) ) )
        drTi = np.asarray( list( itertools.chain.from_iterable( d.atom(a+3,\
                       "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr) ) ) )
        drO1 = np.asarray( list( itertools.chain.from_iterable( d.atom(a+5,\
                       "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr) ) ) )
        drO2 = np.asarray( list( itertools.chain.from_iterable( d.atom(a+7,\
                       "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr) ) ) )
        drO3 = np.asarray( list( itertools.chain.from_iterable( d.atom(a+9,\
                       "%s[1]"%srstr, "%s[2]"%srstr, "%s[3]"%srstr) ) ) )

        print "Atomic Displacements of Ba, Ti, O1, O2, and O3: \n", drBa, \
                "\n", drTi, "\n", drO1, "\n", drO2, "\n", drO3 

        p= np.dot( ZBa, drBa ) + np.dot( ZTi, drTi ) + np.dot( ZO1, drO1) \
          +  np.dot( ZO2, drO2) + np.dot( ZO3, drO3)
        P += 1.60217662 * p * 10.0 / ( 64.0 * n**3 )
    if P[0] < 0. and P[1] < 0. and P[2] < 0.:
        f = -1.
    else:
        f = 1.  
    print "The absolute polarization: ", (np.append( P, [ f*la.norm(P)] )).tolist()
    return (np.append( P, [ f*la.norm(P)] )).tolist()

"""

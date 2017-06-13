from math import *

def volume( cellType, a, b, c, alpha, beta, gama ):
    
    #Tetragonal
    if cellType == "T":
        return a*a*c
    #Orthorhombic    
    elif cellType == "O":
        return a*b*c
    #Cubic
    elif cellType == "C":
        return a*a*a
    #Rhombohedral
    elif cellType == "R":
        alpha = alpha * pi / 180.
        cosValue = cos(alpha)
        temp = a*a*a*(1. - 3 * cosValue**2  ) 
        temp = temp - 2.0 * sqrt( cosValue**3 )
        return temp
    else:
        return "Invalid use of volume function."
        
        
if __name__ == "__main__":
    print volume( "R", 4.01, 4.01, 4.01, 89.81, None, None )

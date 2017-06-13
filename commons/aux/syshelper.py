import os

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...") 
    
def touch(filename, times=None):
    with open(filename, 'w'):
        os.utime(filename, times)

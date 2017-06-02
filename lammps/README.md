Contents
------------------------------------------------------------------------------------------------------------
        README.md
        src/CMakeLists.txt
        CMakeLists.txt
        package.py        

* `spack install lammps` to create libslammps.so

* Move libslammps.so to lammps/python where lammps.py is located.

* Add the following to the PATH in `.bashrc` 
    -`spack/bin`
    -`openmpi/bin`
    -`openmpi/lib`

* Add the following to PYTHONPATH in `.bashrc`
    -`lammps/python`
    -`mpi4py/lib/python2.7/site-packages`

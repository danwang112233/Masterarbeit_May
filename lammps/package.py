from spack import *
import glob
import os
import sys 

class Lammps(Package):
    """A classical molecular dynamics code that models an ensemble of particles"""
    homepage = "lammps.sandia.gov"
    #url      = "http://lammps.sandia.gov/tars/lammps-10.tar.gz"
    #url      = "http://github.com/vishalkenchan/lammps/tree/feature/CORESHELL/wolf"
    url      = "http://github.com/vishalkenchan/lammps/archive/feature/CORESHELL/wolf.zip"
    #url      = "http://lammps.sandia.gov/tars/lammps-stable.tar.gz"
    # lammps releases are named after their release date.
    #version('10May16', '6a70d4b5b76a6c667dc5973dd528fd9d65dcfb7e4729e493c2fbfa12cac2d918' )
    version('wolf', '5be75350f901f34d6b356657f6d0cbd6315464830a6e9b3a854c3241383ae677' )

    variant('mpi',    default=True,  description='Compile with MPI' )
    variant('python', default=True,  description='Compile lammps as a python extension')
    variant('fftw',   default=False, description='Compile with fftw library' )
    variant('jpeg',   default=False, description='Compile with jpeg library' )

    depends_on('cmake')
    # optional dependencies
    extends   ('python',    when='+python')
    depends_on('py-mpi4py', when='+mpi+python')
    depends_on('mpi',       when='+mpi')
    
    # define a function to write CMakeLists into lammps directory
    def add_cmakelists (self):
        """ Install CMakeLists provided with spack into lammps source directory.
        """
        install( join_path(os.path.dirname(self.module.__file__), 'CMakeLists.txt'), '.' )
        install( join_path(os.path.dirname(self.module.__file__), \
                'src', 'CMakeLists.txt'), './src' )

    def include_style_h( self, spec ):
        """ lammps has Install.sh, Depend.sh and Make.sh scripts in the source directory 
            to include approprate header files.
        """
        with working_dir('src'):
            os.system('make yes-class2')
            os.system('make yes-coreshell')
            os.system('make yes-kspace')
            os.system('make yes-misc')
            os.system('make yes-molecule')
            if '+python' in spec:
                os.system('make yes-python')
            os.system('chmod +x Make.sh')
            os.system('./Make.sh style')
    
    def install( self, spec, prefix ):
        options = []
        options.extend( std_cmake_args )
        self.include_style_h( spec )
        self.add_cmakelists()

        mkdirp(self.prefix)
    
        if '+mpi' in spec:
            options.extend( [
                # FIXME: avoid hardcoding mpi wrappers names
                '-DCMAKE_C_COMPILER=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpicc'), 
                '-DCMAKE_CXX_COMPILER=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpic++'),
#                '-DCMAKE_C_COMPILER=%s'   % spec['mpi'].mpicc), 
#                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx),
#' -I%s'  % self.spec['python'].prefix.include
#'-DCMAKE_INCLUDE_RPATH=%s' % join_path(self.spec['python'].prefix.include, 'python2.7')
            ])
        """
        for library in ('gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis'):  # NOQA: ignore=E501
            if library in spec:
                options.extend([
                    '-D%s_DIR=%s' % (library.upper(), spec[library].prefix),
                    '-DDEAL_II_WITH_%s:BOOL=ON' % library.upper()
                ])
            else:
                options.extend([
                    '-DDEAL_II_WITH_%s:BOOL=OFF' % library.upper()
                ])
        """    
            
            
        cmake('.', *options)
        make()
        lib_dsuffix = 'so'
        mkdirp( self.prefix.lib )
        install( join_path( self.stage.source_path,'liblammps.') \
                     + lib_dsuffix, self.prefix.lib )
#        mkdirp( self.prefix.bin )
#        install( join_path(self.stage.source_path, 'src','lmp'), self.prefix.bin)
    """
        1. CMakeLists should be cleaned up and should be standalone. It should not
           depend on Makefiles provided with lammps.
        2. USER packages should have options, but the list is too long to provide 
           it as an option in `spec`.
        3. If you intend to change cmake executable, it is possible my first 
           installing `module` and then do `spack load cmake`. You might want to 
           first let spack wrap module.
    """

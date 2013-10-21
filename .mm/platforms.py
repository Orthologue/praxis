# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


import os


def platform(builder):
    """
    Decorate the {builder} with platform specific options
    """
    # get the platform id
    platform = builder.host.system
    # print('platform:', platform)

    # on darwin
    if platform == 'Darwin':
        # assume macports
        systemdir = '/opt/local'
        systemlibdir = os.path.join(systemdir, 'lib')
        systemincdir = os.path.join(systemdir, 'include')

        # set up {libpq}
        libpqVersion = 'postgresql92'
        # do we have postgres?
        havePostgres = (
            os.path.isdir(os.path.join(systemlibdir, libpqVersion))
            and
            os.path.isdir(os.path.join(systemincdir, libpqVersion))
            )
        # if yes
        if havePostgres:
            # grab it
            libpq = builder.requirements['libpq']
            # set it up
            libpq.environ = {
                'LIBPQ_DIR': systemdir,
                'LIBPQ_LIBDIR': os.path.join(systemlibdir, libpqVersion),
                'LIBPQ_INCDIR': os.path.join(systemincdir, libpqVersion),
                }
            # and its runtime
            libpq.ldpath = os.path.join(systemincdir, libpqVersion)

        # set up {python}
        pythonVersion = '3.3'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(systemdir, 'lib', python),
            'PYTHON_INCDIR': os.path.join(systemdir, 'include', python),
            }

        # all done
        return builder

    # on linux
    if platform == 'Linux':
        # on normal distributions
        systemdir = '/usr'
        systemlibdir = os.path.join(systemdir, 'lib')
        systemincdir = os.path.join(systemdir, 'include')

        # set up {libpq}
        libpqVersion = 'postgresql'
        # do we have postgres?
        havePostgres = (
            os.path.isfile(os.path.join(systemlibdir, 'libpq.so'))
            and
            os.path.isdir(os.path.join(systemincdir, libpqVersion))
            )
        # if yes
        if havePostgres:
            # grab it
            libpq = builder.requirements['libpq']
            # set it up
            libpq.environ = {
                'LIBPQ_DIR': systemdir,
                'LIBPQ_INCDIR': os.path.join(systemincdir, libpqVersion),
                'LIBPQ_LIBDIR': systemlibdir,
            }
            # and its runtime
            libpq.ldpath = os.path.join(systemincdir, libpqVersion)

        # set up {python}
        pythonVersion = '3.3'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(systemdir, 'lib', python),
            'PYTHON_INCDIR': os.path.join(systemdir, 'include', python),
            }

        # all done
        return builder

    # on all other platforms
    return builder


# end of file 

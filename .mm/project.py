# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


def requirements(package):
    """
    Build a dictionary with the external dependencies of the {praxis} project
    """

    # build the package instances
    packages = [
        package(name='python', optional=False),
        ]

    # build a dictionary and return it
    return { package.name: package for package in packages }


# end of file

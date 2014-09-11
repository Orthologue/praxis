# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = ecrs

# the list of python modules
EXPORT_PYTHON_MODULES = \
    PunchParser.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

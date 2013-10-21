# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = queries

# the list of python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

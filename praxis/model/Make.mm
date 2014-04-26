# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = model

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Punches.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

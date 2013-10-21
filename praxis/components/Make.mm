# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = components

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Application.py \
    DBApplication.py \
    DBClient.py \
    IDD.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

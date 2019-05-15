# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = schema/base

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Temporary.py \
    Type.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

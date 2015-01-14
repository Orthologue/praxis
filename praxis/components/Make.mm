# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = components

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Action.py \
    Datastore.py \
    IDD.py \
    Layout.py \
    Praxis.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

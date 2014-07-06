# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = actions

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Command.py \
    Debug.py \
    IDD.py \
    Primer.py \
    Staff.py \
    Schedule.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

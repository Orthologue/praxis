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
    Copyright.py \
    Debug.py \
    IDD.py \
    License.py \
    Primer.py \
    Staff.py \
    Schedule.py \
    Version.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

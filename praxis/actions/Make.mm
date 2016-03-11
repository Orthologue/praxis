# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = actions

# the list of python modules
EXPORT_PYTHON_MODULES = \
    About.py \
    Debug.py \
    IDD.py \
    Payroll.py \
    Primer.py \
    Staff.py \
    Schedule.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = queries

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Company.py \
    Employee.py \
    EmployeeListing.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

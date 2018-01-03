# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = vendors/ecrs/reports

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Daily.py \
    Punches.py \
    Staff.py \
    Transactions.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

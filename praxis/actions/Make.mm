# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = actions

# the list of python modules
EXPORT_PYTHON_MODULES = \
    About.py \
    Creator.py \
    Debug.py \
    Destroyer.py \
    IDD.py \
    Payroll.py \
    Primer.py \
    Staff.py \
    Schedule.py \
    Transactions.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

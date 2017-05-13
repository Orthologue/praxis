# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = schema/hr

# the list of python modules
EXPORT_PYTHON_MODULES = \
    Employee.py \
    Employer.py \
    Employment.py \
    EmploymentType.py \
    PayType.py \
    PayFrequency.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

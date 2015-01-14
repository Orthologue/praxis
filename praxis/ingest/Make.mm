# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# the project name
PROJECT = praxis
# the package name
PACKAGE = ingest

# the list of python modules
EXPORT_PYTHON_MODULES = \
    ScheduleParser.py \
    ScheduleScanner.py \
    Staff.py \
    __init__.py

# the standard build targets
all: export

export:: export-package-python-modules

# end of file

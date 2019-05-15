# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = schema

RECURSE_DIRS = \
    base \
    crm \
    hr \
    sales \

# the list of python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# the standard build targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# end of file

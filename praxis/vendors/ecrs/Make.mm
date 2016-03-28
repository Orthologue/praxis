# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = vendors/ecrs
# the list of directories to visit
RECURSE_DIRS = \
    model \
    reports \

# the list of python modules
EXPORT_PYTHON_MODULES = \
    exceptions.py \
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

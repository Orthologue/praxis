# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = praxis
# clean up
PROJ_CLEAN += $(EXPORT_MODULEDIR)

# the list of directories to visit
RECURSE_DIRS = \
    actions \
    components \
    compliance \
    ecrs \
    ingest \
    model \
    queries \
    schema \
    support \

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

export:: __init__.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) __init__.py

# construct my {__init__.py}
__init__.py: __init__py
	@sed -e "s:BZR_REVNO:$$(bzr revno):g" __init__py > __init__.py


# end of file

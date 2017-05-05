# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
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
    hardware \
    ingest \
    model \
    queries \
    schema \
    support \
    vendors \

# get today's date
TODAY = ${strip ${shell date -u}}
# grab the revision number
REVISION = ${strip ${shell bzr revno}}
# if not there
ifeq ($(REVISION),)
REVISION = 0
endif

# the list of python modules
EXPORT_PYTHON_MODULES = \
    exceptions.py \
    meta.py \
    __init__.py

# the standard build targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: meta.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) meta.py

revision: meta.py export-python-modules
	@$(RM) meta.py

# construct my {meta.py}
meta.py: meta Make.mm
	@sed \
          -e "s:MAJOR:$(PROJECT_MAJOR):g" \
          -e "s:MINOR:$(PROJECT_MINOR):g" \
          -e "s:REVISION:$(REVISION):g" \
          -e "s|TODAY|$(TODAY)|g" \
          meta > meta.py

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))


# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = tests

RECURSE_DIRS = \
    compliance \
    ecrs \

# the standard build targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# end of file

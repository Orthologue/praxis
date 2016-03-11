# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = tests

# standard build targets
all: test

# testing
test: sanity

sanity:
	${PYTHON} ./sanity.py

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = tests
# clean up
PROJ_CLEAN += *.eps

all: test clean

test: sanity samples

sanity:
	${PYTHON} ./sanity.py

samples:
	${PYTHON} ./receipt.py

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = tests

all: test

test: sanity compliance

sanity:
	${PYTHON} ./sanity.py

compliance:
	${PYTHON} ./california.py

# end of file

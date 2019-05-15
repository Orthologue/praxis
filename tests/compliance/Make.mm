# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = tests

all: test

test: sanity compliance

sanity:
	${PYTHON} ./sanity.py

compliance:
	${PYTHON} ./california.py

# end of file

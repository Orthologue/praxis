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

test: sanity punches

sanity:
	${PYTHON} ./sanity.py

punches:
	${PYTHON} ./punch_create.py
	${PYTHON} ./punch_parse.py

# end of file

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

test: sanity punches staff

sanity:
	${PYTHON} ./sanity.py

punches:
	${PYTHON} ./punch_create.py
	${PYTHON} ./punch_parse.py

staff:
	${PYTHON} ./staff.py

# end of file

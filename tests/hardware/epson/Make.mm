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
# clean up
PROJ_CLEAN += *.eps

all: test clean

test: sanity samples info

sanity:
	${PYTHON} ./sanity.py

samples:
	${PYTHON} ./receipt.py
	${PYTHON} ./barcode.py

info:
	${PYTHON} ./fonts.py

# end of file

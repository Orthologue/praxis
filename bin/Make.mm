# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = bin

# the configuration files
EXPORT_BINS = \
    praxis

# the standard build targets
all: export

export:: export-binaries


# end of file

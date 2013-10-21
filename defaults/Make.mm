# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = defaults

# the configuration files
EXPORT_ETC = \
    praxis.cfg

# the standard build targets
all: export

export:: export-etc

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = defaults

# the configuration files
EXPORT_ETC = \
    praxis.cfg

# the standard build targets
all: export

export:: export-etc


# end of file

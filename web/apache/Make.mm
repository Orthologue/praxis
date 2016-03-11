# -*- Makefile -*-
#
# michael a.g. aivazis
# orthologue
# (c) 1998-2016 all rights reserved
#


# project defaults
PROJECT = praxis
# the package name
PACKAGE = apache

# the standard build targets
all: tidy

live: live-apache-conf live-apache-restart

# there is another target that might be useful:
#
#    live-apache-conf: make a link to the configuration file in the apache {sites-available}
#                      directory, followed by enabling the site

# end of file

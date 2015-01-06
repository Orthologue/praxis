# -*- Makefile -*-
#
# michael a.g. aivazis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = praxis
PACKAGE = /etc/apache2/sites-available

#--------------------------------------------------------------------------
#
all: tidy

#--------------------------------------------------------------------------
#

RSYNC = /usr/bin/rsync -ruavz --progress --stats
FILES = praxis
WEB_USER = root@praxis.orthologue.com
WEB_LOCATION = $(PACKAGE)

deploy: tidy
	$(RSYNC) $(FILES) $(WEB_USER):$(WEB_LOCATION)


# end of file

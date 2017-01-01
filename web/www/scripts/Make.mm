# -*- Makefile -*-
#
# michael a.g. aivazis
# orthologue
# (c) 1998-2017 all rights reserved
#


PROJECT = praxis
PACKAGE = web/www/scripts

#--------------------------------------------------------------------------
#
all: tidy

#--------------------------------------------------------------------------
#

RSYNC = /usr/bin/rsync --delete -ruavz --progress --stats
FILES = . --exclude=*Make.mm*
WEB_USER = $(PROJECT)@praxis.orthologue.com
WEB_LOCATION = $(PACKAGE)

deploy: tidy
	$(RSYNC) $(FILES) $(WEB_USER):$(WEB_LOCATION)


# end of file

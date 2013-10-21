# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


PROJECT = praxis
PACKAGE = web/html

RECURSE_DIRS = \
    graphics \
    scripts \
    styles \


#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#

RSYNC = /usr/bin/rsync --delete -ruavz --progress --stats
FILES = . --exclude=*Make.mm
WEB_USER = $(PROJECT)@praxis.orthologue.com
WEB_LOCATION = $(PACKAGE)

deploy: tidy
	$(RSYNC) $(FILES) $(WEB_USER):$(WEB_LOCATION)

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


PROJECT = praxis

RECURSE_DIRS = \
    apache \
    bin \
    www \

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
FILES = html --exclude=*Make.mm
WEB_USER = praxis@praxis.orthologue.com
WEB_LOCATION = web

deploy: tidy
	$(RSYNC) $(FILES) $(WEB_USER):$(WEB_LOCATION)

# end of file

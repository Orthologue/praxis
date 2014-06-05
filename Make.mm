# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = praxis

RECURSE_DIRS = \
    praxis \
    defaults \
    bin \
    tests \
    web \
    primer \

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
#  shortcuts to building in my subdirectories
.PHONY: bin defaults praxis primer tests web

bin:
	(cd bin; $(MM))

defaults:
	(cd defaults; $(MM))

praxis:
	(cd praxis; $(MM))

tests:
	(cd tests; $(MM))

web:
	(cd web; $(MM))

build: praxis defaults bin

test: build tests


#--------------------------------------------------------------------------
#
PRAXIS_ZIP = $(EXPORT_ROOT)/praxis-1.0.zip
zip: praxis defaults
	@-$(RM_F) $(PRAXIS_ZIP)
	@(cd $(EXPORT_ROOT)/packages; zip -r ${PRAXIS_ZIP} * )
	@(cd $(EXPORT_ROOT); zip -r ${PRAXIS_ZIP} defaults )


# end of file 

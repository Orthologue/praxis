# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
PROJECT = praxis

RECURSE_DIRS = \
    praxis \
    defaults \
    bin \
    tests \
    web \
    primer \

PRAXIS_ZIP = $(EXPORT_ROOT)/praxis-1.0.zip

# the standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# convenoence
build: praxis defaults bin

test: build tests

# the self-contained build
zip: praxis defaults
	@-$(RM_F) $(PRAXIS_ZIP)
	@(cd $(EXPORT_ROOT)/packages; zip -r ${PRAXIS_ZIP} * )
	@(cd $(EXPORT_ROOT); zip -r ${PRAXIS_ZIP} defaults )

#  shortcuts to building in my subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))

# end of file

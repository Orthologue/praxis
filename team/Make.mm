# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# project defaults
include praxis.def
# package name
PACKAGE = people
# add this to the clean pile
PROJ_CLEAN += authorized_keys
# the list of public keys
PUBLIC_KEYS = $(wildcard *.pub)

# standard targets
all: tidy
# make the autorized keys file
authorized_keys: $(PUBLIC_KEYS) grant.py grant.pfg Make.mm
	./grant.py

live: authorized_keys
	$(SCP) $< $(PROJ_LIVE_ADMIN)@$(PROJ_LIVE_HOST):$(PROJ_LIVE_HOME)/.ssh

# end of file

# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#

# project defaults
PROJECT = praxis
# the package name
PACKAGE = primer

# the standard build targets
all: tidy

# reset the database to a clean state
reset: drop create

# build the database
create:
	@praxis db create
	@praxis db init

# wipe everything clean
drop:
	-@praxis db clear
	-@praxis db drop
	-@$(RM_F) idd.cfg


# the overall target that populates all the database tables
prime: boot

# populate the database with the administrative content
boot:
	praxis db prime

# end of file

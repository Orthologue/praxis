# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#

# project defaults
include praxis.def
# the package name
PACKAGE = primer

# the standard build targets
all: tidy

# reset the database to a clean state
reset: drop create

# build the database
create:
	$(PYTHON) create_database.py
	$(PYTHON) create_tables.py

# wipe everything clean
drop:
	-$(PYTHON) drop_tables.py
	-$(PYTHON) drop_database.py
	-$(RM_F) idd.cfg


# the overall target that populates all the database tables
prime: boot

# populate the database with the administrative content
boot:
	$(PYTHON) prime_static.py

# end of file

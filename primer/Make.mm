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

# initialize the tables
praxis:
	$(PYTHON) prime_static.py

# wipe everything clean
drop:
	-$(PYTHON) drop_tables.py
	-$(PYTHON) drop_database.py
	-$(RM_F) idd.cfg


# the overall target that populates all the database tables
prime: praxis suppliers

# populate the database with the administrative content
praxis:

# add suplier info
suppliers:

# end of file

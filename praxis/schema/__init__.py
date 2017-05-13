# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# get the db support
from .. import db


# literals, for convenience
null = db.null
default = db.default

# pull in the table types
# bases
from . import base
# contact management
from . import crm
# personnel
from . import hr
# products
from . import sales

# support
schema = crm, hr, sales

# table groups
typeTables = tuple(table for category in schema for table in category.typeTables)
atomTables = tuple(table for category in schema for table in category.atomTables)
attributeTables = tuple(table for category in schema for table in category.attributeTables)
relationTables = tuple(table for category in schema for table in category.relationTables)

# the table list, sorted by dependency
tables = typeTables + atomTables + attributeTables + relationTables


# end of file

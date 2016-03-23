# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Location(praxis.db.table, id="locations"):
    """
    Location information
    """

    # data layout
    location = praxis.db.str().primary()
    # postal
    address = praxis.db.str().notNull()
    country = praxis.db.str(default="USA")
    # coördinates
    geo = praxis.db.str(default="0,0")


    # meta-methods
    def __str__(self):
        return "{0.id}: {0.address}".format(self)


# end of file

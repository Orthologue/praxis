# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import praxis
# access to the table of item types
from .ItemType import ItemType


# table declaration
class Item(praxis.db.table, id='items'):
    """
    Item declarations
    """

    # data layout
    eid = praxis.db.str().primary()
    kind = praxis.db.reference(key=ItemType.id).notNull()
    name = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.name}".format(self)


# end of file

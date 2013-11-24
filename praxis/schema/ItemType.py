# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
import praxis


# table declaration
class ItemType(praxis.db.table, id='item_types'):
    """
    A table of the various types of items

    The {description} is interpreted as the name of the table that contains the reference to
    this item. Currently, items are either {products} or {services}.
    """

    # data layout
    id = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.description}".format(self)


# end of file 

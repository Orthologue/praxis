# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class ItemType(Type, id='item_types'):
    """
    A table of the various types of items

    The {description} is interpreted as the name of the table that contains the reference to
    this item. Currently, items are either {products} or {services}.
    """


# end of file

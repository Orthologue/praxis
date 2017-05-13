# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to my superclass
from .. import base


# table declaration
class ItemType(base.type, id='item_types'):
    """
    A table of the various types of items

    The {description} is interpreted as the name of the table that contains the reference to
    this item. Currently, items are either {products} or {services}.
    """


# end of file

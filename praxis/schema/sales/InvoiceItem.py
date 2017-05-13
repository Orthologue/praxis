# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# refrenced tables
from .Invoice import Invoice


# table declaration
class InvoiceItem(praxis.db.table, id='invoice_items'):
    """
    Item declarations
    """

    # data layout
    id = praxis.db.str().primary()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.name}".format(self)


# end of file

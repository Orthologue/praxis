# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Phone(praxis.db.table, id="phones"):
    """
    Phone numbers
    """

    # data layout
    id = praxis.db.str().primary()
    # phone number parts
    number = praxis.db.str().notNull()
    extension = praxis.db.str(default=praxis.db.null)


# end of file 

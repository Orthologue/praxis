# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Phone(praxis.db.table, id="phones"):
    """
    Phone numbers
    """

    # phone number
    number = praxis.db.str().primary()


# end of file

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Email(praxis.db.table, id="emails"):
    """
    Email addresses
    """

    # data layout
    id = praxis.db.str().primary()
    # email
    email = praxis.db.str().notNull()


# end of file

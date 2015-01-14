# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import praxis


# table declaration
class URI(praxis.db.table, id="uris"):
    """
    Universal resource identifiers
    """

    # data layout
    id = praxis.db.str().primary()
    # uri
    uri = praxis.db.str().notNull()


# end of file

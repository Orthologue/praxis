# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# access to the framework
import praxis


# table declaration
class URI(praxis.db.table, id="uris"):
    """
    Universal resource identifiers
    """

    # uri
    uri = praxis.db.str().primary()


# end of file

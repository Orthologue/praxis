# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Email(praxis.db.table, id="emails"):
    """
    Email addresses
    """

    # email
    email = praxis.db.str().primary()


# end of file

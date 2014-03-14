# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis


# table declaration
class EmailType(praxis.db.table, id='email_types'):
    """
    A table of the various types of email
    """

    # data layout
    id = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.description}".format(self)


# end of file 

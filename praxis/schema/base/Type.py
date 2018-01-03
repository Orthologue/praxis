# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# access to the framework
import praxis


# table declaration
class Type(praxis.db.table):
    """
    Support for enabling a limited form of polymorphism among database tables
    """


    # data layout
    type = praxis.db.str().primary()
    description = praxis.db.str().notNull()


    # meta-methods
    def __str__(self):
        return "{0.type}: {0.description}".format(self)


# end of file

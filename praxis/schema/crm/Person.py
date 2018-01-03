# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# access to the framework
import praxis
# access to the table of entities
from .Entity import Entity


# table declaration
class Person(praxis.db.table, id='people'):
    """
    Basic people information
    """

    # people are entities
    entity = praxis.db.reference(key=Entity.entity).primary()

    # data layout
    first = praxis.db.str().notNull()
    middle = praxis.db.str()
    last = praxis.db.str().notNull()
    preferred = praxis.db.str()


    # meta-methods
    def __str__(self):
        return "{0.entity}: {0.first} {0.last}".format(self)


# end of file

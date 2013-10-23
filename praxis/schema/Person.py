# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
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

    entity = praxis.db.reference(key=Entity.eid).primary()

    first = praxis.db.str().notNull()
    middle = praxis.db.str()
    last = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.entity}: {0.first} {0.last}".format(self)


# end of file 

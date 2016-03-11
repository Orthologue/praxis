# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# access to the table of entities
from .Entity import Entity


# table declaration
class Company(praxis.db.table, id='companies'):
    """
    Company information
    """

    # data layout
    entity = praxis.db.reference(key=Entity.eid).primary()
    name = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.entity}: {0.name}".format(self)


# end of file

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis
# access to the table of entity types
from .EntityType import EntityType


# table declaration
class Entity(praxis.db.table, id='entities'):
    """
    Entity declarations
    """

    # data layout
    eid = praxis.db.str().primary()
    kind = praxis.db.reference(key=EntityType.id).notNull()
    name = praxis.db.str().notNull()
    
    # meta-methods
    def __str__(self):
        return "{0.id}: {0.name}".format(self)


# end of file 

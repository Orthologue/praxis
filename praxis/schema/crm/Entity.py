# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
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
    entity = praxis.db.str().primary()
    type = praxis.db.reference(key=EntityType.type).notNull()


# end of file

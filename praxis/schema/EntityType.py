# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis


# table declaration
class EntityType(praxis.db.table, id='entity_types'):
    """
    A table of the various types of entities

    The {description} is interpreted as the name of the table that contains the reference to
    this entity. Currently, entities are either {people} or {companies}.
    """

    # data layout
    id = praxis.db.str().primary()
    description = praxis.db.str().notNull()

    # meta-methods
    def __str__(self):
        return "{0.id}: {0.description}".format(self)


# end of file

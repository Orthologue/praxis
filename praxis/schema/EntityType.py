# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from .Type import Type


# table declaration
class EntityType(Type, id='entity_types'):
    """
    A table of the various types of entities

    The {description} is interpreted as the name of the table that contains the reference to
    this entity. Currently, entities are either {people} or {companies}.

    The current primer fills this table with the following values:
        companies, people
    """


# end of file

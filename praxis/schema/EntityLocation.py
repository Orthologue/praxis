# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .Location import Location
from .LocationType import LocationType


# table declaration
class EntityLocation(Temporary, id='entity_locations'):
    """
    Physical locations associated with entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with a location
    entity = praxis.db.reference(key=Entity.eid).notNull()
    location = praxis.db.reference(key=Location.id).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=LocationType.id).notNull()


# end of file 

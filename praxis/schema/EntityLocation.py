# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .Location import Location
from .ContactPurpose import ContactPurpose


# table declaration
class EntityLocation(Temporary, id='entity_locations'):
    """
    Physical locations associated with entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with a location
    entity = praxis.db.reference(key=Entity.entity).notNull()
    location = praxis.db.reference(key=Location.location).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=ContactPurpose.purpose).notNull()


# end of file

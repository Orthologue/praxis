# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the framework
import praxis
# my superclass
from .Temporary import Temporary
# and the tables i refer to
from .Entity import Entity
from .URI import URI
from .URIType import URIType


# table declaration
class EntityURI(Temporary, id='entity_uris'):
    """
    URIs associated with entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity with a URI
    entity = praxis.db.reference(key=Entity.eid).notNull()
    uri = praxis.db.reference(key=URI.id).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=URIType.id).notNull()


# end of file 

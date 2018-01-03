# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# access to the framework
import praxis
# access to my superclass
from .. import base
# and the tables i refer to
from .Entity import Entity
from .URI import URI
from .URIType import URIType
from .ContactPurpose import ContactPurpose


# table declaration
class EntityURI(base.temporary, id='entity_uris'):
    """
    URIs associated with entities
    """

    # don't forget that this table derives from {Temporary}, hence it describes a relationship
    # with a potentially finite duration

    # associating an entity
    entity = praxis.db.reference(key=Entity.entity).notNull()
    # with a URI
    uri = praxis.db.reference(key=URI.uri).notNull()
    # of a particular kind
    type = praxis.db.reference(key=URIType.type).notNull()
    # for a particular purpose
    purpose = praxis.db.reference(key=ContactPurpose.purpose).notNull()


# end of file
